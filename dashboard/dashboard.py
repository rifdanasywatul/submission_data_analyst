import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Helper functions
def load_data():
    day_df = pd.read_csv("dataset/day.csv")
    hour_df = pd.read_csv("dataset/hour.csv")
    
    # Konversi kolom dteday ke datetime
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

# Fungsi untuk menghitung total penyewaan per bulan
def calculate_monthly_performance(day_df):
    monthly_performance = day_df.groupby(day_df['dteday'].dt.to_period('M')).agg({
        'cnt': 'sum'
    }).reset_index()
    monthly_performance['dteday'] = monthly_performance['dteday'].dt.to_timestamp()
    return monthly_performance

# Fungsi untuk menghitung rata-rata penyewaan per bulan
def calculate_monthly_avg(day_df):
    monthly_avg = day_df.groupby(day_df['dteday'].dt.to_period('M')).agg({
        'casual': 'mean',
        'registered': 'mean'
    }).reset_index()
    monthly_avg['dteday'] = monthly_avg['dteday'].dt.to_timestamp()
    return monthly_avg

# Fungsi untuk menghitung total penyewaan berdasarkan hari dalam seminggu
def calculate_weekday_usage(hour_df):
    weekday_usage = hour_df.groupby(by="weekday").agg({
        "cnt": "sum"
    }).reset_index()
    return weekday_usage

# Fungsi untuk menghitung total penyewaan berdasarkan kondisi cuaca
def calculate_weather_clustering(hour_df):
    weather_clustering = hour_df.groupby(by="weathersit").agg({
        'cnt': 'sum',
        'temp': 'mean',
        'hum': 'mean'
    }).reset_index()
    return weather_clustering

# Load data
day_df, hour_df = load_data()

# Create Streamlit app
col1, col2 = st.columns([1, 4])  # Membuat dua kolom dengan proporsi yang berbeda
with col1:
    # Tambahkan logo di bagian kiri
    logo_path = "bike-sharing-logo.png"
    st.image(logo_path, use_column_width=True)
with col2:
    st.title("Bike Sharing Data Dashboard")

# Sidebar filter
st.sidebar.header("Filter Options")
selected_year = st.sidebar.selectbox("Select Year", options=day_df['dteday'].dt.year.unique())

# Filter data berdasarkan tahun
filtered_data = day_df[day_df['dteday'].dt.year == selected_year]

# Show monthly performance
monthly_performance = calculate_monthly_performance(filtered_data)
st.subheader("Monthly Performance")
fig, ax = plt.subplots()
ax.plot(monthly_performance['dteday'], monthly_performance['cnt'], marker='o', linestyle='-', color='blue')
ax.set_title('Monthly Performance for Year ' + str(selected_year))
ax.set_xlabel('Date')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Show average usage
monthly_avg = calculate_monthly_avg(filtered_data)
st.subheader("Average Usage")
fig, ax = plt.subplots()
monthly_avg.plot(x='dteday', y=['casual', 'registered'], kind='bar', ax=ax, color=['orange', 'blue'])
ax.set_title('Average Rentals per Month for Year ' + str(selected_year))
ax.set_xlabel('Month')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

# Show weekday usage
weekday_usage = calculate_weekday_usage(hour_df)
st.subheader("Weekday Usage")
fig, ax = plt.subplots()
ax.bar(weekday_usage['weekday'], weekday_usage['cnt'], color='lightgreen')
ax.set_title('Total Rentals by Day of the Week for Year ' + str(selected_year))
ax.set_xlabel('Day of the Week (0: Sunday, 6: Saturday)')
ax.set_ylabel('Total Rentals')
ax.set_xticks(weekday_usage['weekday'])  # Menampilkan label hari
st.pyplot(fig)

# Show weather clustering
weather_clustering = calculate_weather_clustering(hour_df)
st.subheader("Weather Clustering")
fig, ax = plt.subplots()
sns.barplot(data=weather_clustering, x='weathersit', y='cnt', palette='coolwarm', ax=ax)
ax.set_title('Total Rentals by Weather Conditions for Year ' + str(selected_year))
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Total rentals by hour of the day
st.subheader("Total Rentals by Hour of the Day")
hourly_usage = hour_df.groupby('hr').agg({'cnt': 'sum'}).reset_index()
fig, ax = plt.subplots()
ax.plot(hourly_usage['hr'], hourly_usage['cnt'], marker='o', linestyle='-', color='blue')
ax.set_title('Total Rentals by Hour of the Day for Year ' + str(selected_year))
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Total Rentals')
st.pyplot(fig)

# Show additional statistics
st.subheader("Summary Statistics")
st.write(filtered_data.describe())
