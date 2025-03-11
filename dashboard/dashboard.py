import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/felixtaslim2/analisis_data_bikesharing/refs/heads/main/dashboard/day_cleaned.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/felixtaslim2/analisis_data_bikesharing/refs/heads/main/dashboard/hour_cleaned.csv")

st.title('Belajar Analisis Data')
st.header('[Bike Sharing Dataset]')

tab1, tab2, tab3 = st.tabs(["Overview", "Case 1", "Case 2"])

with tab1:
    st.header("Overview")
    st.text("Bike Sharing Dataset merupakan dataset yang berisi data rental sepeda di sebuah Perusahaan Rental Sepeda. Terdapat dua dataset yang digunakan, yaitu day.csv dan hour.csv.")
    
    st.subheader("Day Dataset")
    st.write(day_df.head())

    st.subheader("Hour Dataset")
    st.write(hour_df.head())
    

with tab2:
    st.header("Case 1:")
    st.subheader("Pada musim/season apa sebaiknya dilakukan promosi untuk mencegah penurunan jumlah rental sepeda?")

    # Filter tahun
    selected_year = st.selectbox("Pilih Tahun", options=[2011, 2012])
    # Konversi tahun ke format dataset (0 untuk 2011, 1 untuk 2012)
    year_map = {2011: 0, 2012: 1}
    filtered_df = day_df[day_df['yr'] == year_map[selected_year]]
    # Hitung rata-rata rental sepeda per musim
    byseason_avg = filtered_df.groupby("season")["cnt"].mean()
    season_order = ["Spring", "Summer", "Fall", "Winter"]
    byseason_avg = byseason_avg.reindex(season_order)
    # Buat plot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(byseason_avg.index, byseason_avg.values, marker='o', linestyle='-', color='b', label="Avg Rentals")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Rental Sepeda")
    ax.set_title(f"Tren Rata-rata Rental Sepeda per Musim ({selected_year})")
    ax.grid(True)
    ax.legend()
    # Menampilkan plot
    st.pyplot(fig)

    # Hitung rata-rata jumlah rental sepeda per musim
    byseason_df = day_df.groupby('season')['cnt'].mean().sort_values()
    # Buat plot
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=byseason_df.index, y=byseason_df.values, palette="cool", ax=ax)
    ax.set_title("Rata-rata Jumlah Rental Sepeda per Musim (2011-2012)")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Jumlah Rental Sepeda")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Menampilkan plot
    st.pyplot(fig)

    st.text("Berdasarkan grafik di atas, Spring merupakan musim/season dengan rata-rata jumlah rental sepeda paling rendah. Untuk mencegah penurunan jumlah rental sepeda, maka dianjurkan untuk melakukan promosi pada musim/season Spring.")


with tab3:
    st.header("Case 2: ")
    st.subheader("Kapan jam sepi untuk melaksanakan Happy Hour untuk meningkatkan rental sepeda?")
    
    # Filter tanggal
    selected_date = st.date_input("Pilih Tanggal", value=pd.to_datetime("2011-01-01"))
    # Filter data berdasarkan tanggal yang dipilih
    filtered_hourly_df = hour_df[hour_df["dteday"] == selected_date.strftime("%Y-%m-%d")]
    hourly_avg = filtered_hourly_df.groupby("hr")["cnt"].mean()
    # Plot line chart
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(hourly_avg.index, hourly_avg.values, marker='o', linestyle='-', color='b', label="Avg Rentals")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Rata-rata Rental Sepeda")
    ax.set_title(f"Tren Rata-rata Rental Sepeda per Jam ({selected_date.strftime('%Y-%m-%d')})")
    ax.set_xticks(range(0, 24))
    ax.grid(True)
    ax.legend()
    
    # Menampilkan plot
    st.pyplot(fig)

    #Hitung rata-rata jumlah rental sepeda dari jamnya
    byhour_df = hour_df.groupby("hr")["cnt"].mean()

    #Buat plot
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(x=byhour_df.index, y=byhour_df.values, marker="o", linewidth=2, ax=ax)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Jam dalam Sehari")
    ax.set_ylabel("Rata-rata Jumlah Rental Sepeda (2011-2012)")
    ax.set_title("Tren Jumlah Rental Sepeda Berdasarkan Jam (2011-2012)")
    ax.grid(True)

    #Menampilkan plot
    st.pyplot(fig)

    st.text("""Berdasarkan grafik di atas, terdapat 3 momen rental sepeda sepi:
            
* Jam Sibuk (10:00 - 12:00)
* Malam-Pagi (20:00 - 06:00)
            
Happy hour bisa dilakukan di jam-jam tersebut, entah "Happy Hour Pagi" ataupun "Happy Hour Jam Sibuk". Untuk "Happy Hour Malam" tidak disarankan karena diskon di jam ini tidak cukup menarik pelanggan karena mungkin mereka sedang beristirahat/tidak berniat menyewa, serta malam hari lebih berisiko bagi pesepeda karena kurangnya penerangan dan potensi bahaya(aksi kriminal).""")
