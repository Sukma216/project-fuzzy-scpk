import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl

st.sidebar.title("Projek Akhir SCPK")
st.sidebar.header("About Us")
with st.sidebar.expander("Kelompok 7"):
    st.write("Nama : Dzahabia S Anjani")
    st.write("NIM : 123240037")
    st.write("Nama : Sukmawati Kharisma Gati")
    st.write("NIM : 123240137")
st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Pilih salah satu",
    ["Home", "Data", "Input", "Output"]
)
st.sidebar.header("""📬 Contact Us

📧 Email: sukmajia@email.com  
📱 WhatsApp: 08xxxxxxxxxx  
🏫 UPN Veteran Yogyakarta  
""")

if page == "Home" :
    st.title("Sistem Pendukung Keputusan Pemilihan Pekerjaan Berdasarkan Jurusan")

elif page == "Data" :
    try:
        # buat ngebaca isi dataset 
        df_asli = pd.read_csv("career_change_prediction_dataset.csv")

        # ini buat sortir data pekerjaan dan jurusan apa aja yang ada di dataset 
        pekerjaan_unik = df_asli['Current Occupation'].dropna().unique()
        jurusan_unik = df_asli['Field of Study'].dropna().unique()

        col1, col2, col3 = st.columns(3)
        with col1:
            # ini buat nampilin jumlah total baris yg ada di dataset 
            st.metric(label="Total Baris Data", value=f"{len(df_asli):,}")
        with col2:
            # ini ngitung jumlah pekerjaan yang ada di dataset (yg sudah di sortir)
            st.metric(label="Jumlah Pekerjaan", value=len(pekerjaan_unik))
        with col3:
            # ini ngitung jumlah jurusan yang ada di dataset (yg sudah di sortir)
            st.metric(label="Jumlah Jurusan", value=len(jurusan_unik))

        with st.expander("🔍 Lihat Daftar Semua Pekerjaan & Jurusan yang Ada di Dataset"):
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Pekerjaan:**")
                st.write(", ".join(sorted(pekerjaan_unik)))
            with c2:
                st.markdown("**Jurusan:**")
                st.write(", ".join(sorted(jurusan_unik)))

        st.write("---")

        # Fitur Search Berdasarkan Jurusan atau Pekerjaan
        st.subheader("🔎 Fitur Pencarian & Hubungan Data")

        search_col1, search_col2 = st.columns(2)
        with search_col1:
            search_jurusan = st.text_input("Cari berdasarkan Jurusan (Field of Study):", "", placeholder="Misal: Medicine, Education...")
        with search_col2:
            search_pekerjaan = st.text_input("Cari berdasarkan Pekerjaan (Current Occupation):", "", placeholder="Misal: Business Analyst, Economist...")

        # logika filter data
        df_filtered = df_asli.copy()
        status_pencarian = False

        # kalo user nyari berdasarkan jurusan
        if search_jurusan:
            df_filtered = df_filtered[df_filtered['Field of Study'].str.contains(search_jurusan, case=False, na=False)]
            status_pencarian = True

        # Jikalka user mencari berdasarkan pekerjaan
        if search_pekerjaan:
            df_filtered = df_filtered[df_filtered['Current Occupation'].str.contains(search_pekerjaan, case=False, na=False)]
            status_pencarian = True

        # 5. Menampilkan Tabel Hasil
        if status_pencarian:
            st.success(f"📋 Menampilkan hasil pencarian: Ditemukan {len(df_filtered):,} baris data.")
            
            # Penjelasan otomatis sesuai ide kamu:
            if search_jurusan and not search_pekerjaan:
                st.info(f"💡 **Analisis:** Menampilkan daftar pekerjaan apa saja yang diambil oleh lulusan jurusan **'{search_jurusan}'**.")
            elif search_pekerjaan and not search_jurusan:
                st.info(f"💡 **Analisis:** Menampilkan latar belakang jurusan apa saja yang pernah bekerja sebagai **'{search_pekerjaan}'**.")
                
            # Tampilkan semua data hasil filter pencarian
            st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
        else:
            # Jika tidak ada pencarian, hanya tampilkan 10 data teratas sesuai idemuu
            st.info("Kotak pencarian kosong. Menampilkan **10 Data Teratas** pada dataset:")
            df_top10 = df_asli.head(10).reset_index(drop=True)
            df_top10.index = df_top10.index + 1 # Agar nomor mulai dari 1
            st.dataframe(df_top10, use_container_width=True)

    except FileNotFoundError:
        st.error("File CSV tidak ditemukan, pastikan file 'data_pekerjaan.csv' berada di folder yang sama.")
elif page == "Input" :
    st.title("Input Data Kriteria")
    st.write("Masukkan bobot untuk setiap kriteria berikut:")
    
    gaji_bobot = st.slider("Bobot Gaji Rata-rata", 0.0, 1.0, 0.5)
    kesulitan_bobot = st.slider("Bobot Tingkat Kesulitan", 0.0, 1.0, 0.5)
elif page == "Output" :
    st.title("Hasil Rekomendasi Pekerjaan")
    st.write("Berdasarkan bobot yang Anda masukkan, berikut adalah rekomendasi pekerjaan untuk Anda:")
    
    # Contoh perhitungan sederhana (bobot * nilai)
    df["Skor"] = (df["Gaji Rata-rata (Juta Rupiah)"] * gaji_bobot) - (df["Tingkat Kesulitan"] * kesulitan_bobot)
    df_sorted = df.sort_values(by="Skor", ascending=False)
    
    st.dataframe(df_sorted[["Pekerjaan", "Skor"]])