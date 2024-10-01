import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


 # Memasukan day.csv dan hour.csv pada filenya
daydf = pd.read_csv('Dashboard/day.csv')
daydf['dteday'] = pd.to_datetime(daydf['dteday']) 

hourdf = pd.read_csv('Dashboard/hour.csv')
hourdf['dteday'] = pd.to_datetime(hourdf['dteday']) 




# Judul aplikasi
st.title("Analisis Penyewaan Sepeda per hari apa Berdasarkan Rentang Hari")

# Sidebar untuk memilih rentang waktu
st.sidebar.header("Rentang Waktu Penyewaan Sepeda")
start_date = st.sidebar.date_input("Pilih Tanggal Mulai", value=pd.to_datetime("2011-01-01"))
end_date = st.sidebar.date_input("Pilih Tanggal Akhir", value=pd.to_datetime("2011-12-31"))

# Filter daydf berdasarkan rentang waktu yang dipilih
filtered_data = daydf[(daydf['dteday'] >= pd.to_datetime(start_date)) & (daydf['dteday'] <= pd.to_datetime(end_date))]

# Menampilkan jumlah total penyewaan selama rentang waktu yang dipilih
st.subheader(f"Total Penyewaan Sepeda dari {start_date} hingga {end_date}: {filtered_data['cnt'].sum()}")


# Hitung rata-rata penyewaan sepeda per hari dalam seminggu
rentals_by_weekday = filtered_data.groupby(filtered_data['weekday'])['cnt'].mean()

# Menemukan hari dengan nilai penyewaan tertinggi dan terendah
max_value_idx = rentals_by_weekday.idxmax()
min_value_idx = rentals_by_weekday.idxmin()

# Membuat warna khusus untuk nilai minimum dan maksimum
colors = ['#1f77b4'] * 7
colors[max_value_idx] = '#f21a1a'  # Merah untuk hari dengan penyewaan tertinggi
colors[min_value_idx] = '#a8f7f5'  # Biru terang untuk hari dengan penyewaan terendah

# Membulatkan nilai minimum dan maksimum ke ratusan terdekat
min_y_value = rentals_by_weekday.min() * 0.5  # Kurangi 50% dari nilai terkecil
max_y_value = (rentals_by_weekday.mean() + (rentals_by_weekday.mean() * 0.3) )   # Batas atas ditambahkan 30% dari mean

# Mendefinisikan hari pada setiap angka (0-6)
hari = ['Minggu', 'Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu']

# Membuat barplot untuk rata-rata jumlah penyewaan per hari dalam seminggu
plt.figure(figsize=(10, 6))
plt.bar(rentals_by_weekday.index, rentals_by_weekday.values, color=colors)

# Membuat y-axis awal dan akhir
plt.ylim(min_y_value, max_y_value)

# Membuat custom y-axis 
y_range = max_y_value - min_y_value
optimal_ticks = 6  # Jumlah ticks optimal (antara 5 hingga 10)
tick_interval = (y_range / optimal_ticks)
plt.yticks(ticks=range(int(min_y_value), int(max_y_value), int(tick_interval)))

# Membuat label plot dan judulnya
plt.xlabel('Hari')
plt.ylabel('Rata-rata jumlah penyewaan sepeda')
plt.title('Rata-rata penyewaan sepeda per hari')

# Mengubah x-ticks agar menampilkan nama hari (Senin hingga Minggu)
plt.xticks(ticks=range(7), labels=['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'])

# Menampilkan plot
st.pyplot(plt)
# Membuat informasi paling rendah dan tinggi
st.subheader(f"Hari penyewaan paling rendah pada hari = {hari[(rentals_by_weekday.idxmin()+1)%7]}")
st.subheader(f"Hari penyewaan paling tinggi pada hari = {hari[(rentals_by_weekday.idxmax()+1)%7]}")

# Fungsi untuk mengelompokkan suhu ke dalam kategori
def hour(temp):
    if temp < 0.34:
        return 'Very Cold'
    elif 0.34 <= temp < 0.5:
        return 'Cold'
    elif 0.5 <= temp < 0.66:
        return 'Neutral'
    else:
        return 'Hot'

# Tambahkan kolom kategori suhu pada csv
hourdf['temp_category'] = hourdf['temp'].apply(hour)

# Judul yang akan dibuat
st.title("Analisis Penyewaan Sepeda Berdasarkan Kategori Suhu pada jam")

# Memfilter data hour pada range yang sudah dipilih
filtered_hour_data = hourdf[(hourdf['dteday'] >= pd.to_datetime(start_date)) & (hourdf['dteday'] <= pd.to_datetime(end_date))]

# Menghitung total penyewaan dan kelompokkan atau group by berdasarkan kategori suhu
rentals_by_temp = filtered_hour_data.groupby('temp_category')['cnt'].sum().reset_index()

st.subheader(f"Total Penyewaan Sepeda Berdasarkan Kategori Suhu dari {start_date} hingga {end_date}")

# Membuat plot
fig, ax = plt.subplots(figsize=(10, 6))

# Menggunakan warna yang berbeda untuk setiap kategori suhu
colors = ['#1186f1', '#97C826', '#f7b731', '#e41a1c']

# Membuat bar chart
ax.bar(rentals_by_temp['temp_category'], rentals_by_temp['cnt'], color=colors)

# Menambahkan label dengan judul
ax.set_xlabel('Kategori Suhu', fontsize=12)
ax.set_ylabel('Total Penyewaan Sepeda', fontsize=12)
ax.set_title('Total Penyewaan Sepeda Berdasarkan Kategori Suhu', fontsize=14)

# Set y-axis agar bernilai integer
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: int(x)))

# Tampilkan plot di Streamlit
st.pyplot(fig)

# Tampilkan data dalam tabel
st.subheader('Tabel Data: Total Penyewaan Sepeda Berdasarkan Kategori Suhu')
st.write(rentals_by_temp)
