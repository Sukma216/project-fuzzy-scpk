import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# ini baca file csv nya
nama_file = "career_change_prediction_dataset.csv"

try:
    df_asli = pd.read_csv(nama_file)
    # Biar yang tampil cuma nama jenis pekerjaannya aja, bukan semua baris data
    pekerjaan_unik = df_asli['Current Occupation'].dropna().unique()
    jurusan_unik = df_asli['Field of Study'].dropna().unique()
    list_jurusan = sorted(jurusan_unik)
    csv_ready = True
except FileNotFoundError:
    st.error(f"File CSV '{nama_file}' tidak ditemukan!")
    df_asli = None
    pekerjaan_unik = []
    jurusan_unik = []
    list_jurusan = ["Medicine", "Education", "Informatics"]
    csv_ready = False

# sidebar dan profile 
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

# HOME
if page == "Home" :
    st.title("Sistem Pendukung Keputusan Pemilihan Pekerjaan Berdasarkan Jurusan")
    st.write("Selamat datang di Aplikasi SPK Kelompok 7. Silakan buka menu **Data** untuk eksplorasi atau menu **Input** untuk menghitung rekomendasi.")

# DATA 
elif page == "Data" :
    st.title("📊 Dataset")
    
    if csv_ready:
        col1, col2, col3 = st.columns(3)
        with col1:
            # ini buat nampilin jumlah baris data yang ada di dataset
            st.metric(label="Total Baris Data", value=f"{len(df_asli):,}")
        with col2:
            # buat nampilin jumalh pekerjaan yang sudah disortir
            st.metric(label="Jumlah Pekerjaan", value=len(pekerjaan_unik))
        with col3:
            # buat nampilin jumlah jurusan yang sudah disortir
            st.metric(label="Jumlah Jurusan", value=len(jurusan_unik))

        with st.expander("🔍 Lihat Daftar Semua Pekerjaan & Jurusan yang Ada di Dataset"):
            c1, c2 = st.columns(2)
            with c1:
                # buat nampilin ada pekerjaan apa saja yg ada di dataset (udah disortir)
                st.markdown("**Pekerjaan:**")
                st.write(", ".join(sorted(pekerjaan_unik)))
            with c2:
                # buat nampilin ada jurusan apa saja yg ada di dataset (udah disortir)
                st.markdown("**Jurusan:**")
                st.write(", ".join(sorted(jurusan_unik)))

        st.write("---")

        # fitur search berdasarkan jurusan atau pekerjaan
        st.subheader("🔎 Fitur Pencarian & Hubungan Data")

        search_col1, search_col2 = st.columns(2)
        with search_col1:
            search_jurusan = st.text_input("Cari berdasarkan Jurusan (Field of Study):", "", placeholder="Misal: Medicine, Education...")
        with search_col2:
            search_pekerjaan = st.text_input("Cari berdasarkan Pekerjaan (Current Occupation):", "", placeholder="Misal: Business Analyst, Economist...")

        df_filtered = df_asli.copy()
        status_pencarian = False

        if search_jurusan:
            df_filtered = df_filtered[df_filtered['Field of Study'].str.contains(search_jurusan, case=False, na=False)]
            status_pencarian = True

        if search_pekerjaan:
            df_filtered = df_filtered[df_filtered['Current Occupation'].str.contains(search_pekerjaan, case=False, na=False)]
            status_pencarian = True

        if status_pencarian:
            st.success(f"📋 Menampilkan hasil pencarian: Ditemukan {len(df_filtered):,} baris data.")
            if search_jurusan and not search_pekerjaan:
                st.info(f"💡 **Analisis:** Menampilkan daftar pekerjaan apa saja yang diambil oleh lulusan jurusan **'{search_jurusan}'**.")
            elif search_pekerjaan and not search_jurusan:
                st.info(f"💡 **Analisis:** Menampilkan latar belakang jurusan apa saja yang pernah bekerja sebagai **'{search_pekerjaan}'**.")
            st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
        else:
            st.info("Kotak pencarian kosong. Menampilkan **10 Data Teratas** pada dataset:")
            df_top10 = df_asli.head(10).reset_index(drop=True)
            df_top10.index = df_top10.index + 1
            st.dataframe(df_top10, use_container_width=True)
    else:
        st.error("Tidak dapat memuat halaman Data karena file CSV tidak ada.")

# INPUT 
elif page == "Input" :

    st.title("🧮 Input Data (Fuzzy Mamdani)")
    st.write("Aplikasi ini mendukung pemilihan jumlah kriteria dan alternatif secara dinamis menggunakan selectbox berantai.")

    if csv_ready and df_asli is not None:
        # milih jurusan
        jurusan_user = st.selectbox("🎯 Pilih Latar Belakang Jurusan Kamu:", list_jurusan)
        st.session_state['jurusan_user'] = jurusan_user
        
        # Ambil daftar semua pekerjaan unik yang valid untuk jurusan tersebut dari CSV
        df_filter_jurusan = df_asli[df_asli['Field of Study'] == jurusan_user]
        daftar_alternatif_riil = sorted(list(df_filter_jurusan['Current Occupation'].dropna().unique()))
        
        st.write("---")
        
        # input jumlah kriteria dan alternatif
        st.subheader("Input Jumlah Kriteria")
        col_set1, col_set2 = st.columns(2)
        
        with col_set1:
            # input jumlah kriteria
            jumlah_kriteria = st.number_input(
                label="Masukkan jumlah kriteria (Min: 2, Max: 6):",
                min_value=2, max_value=6, value=3, step=1
            )
        with col_set2:
            # input jumlah alternatif 
            max_alternatif_tersedia = min(len(daftar_alternatif_riil), 10)
            jumlah_alternatif = st.number_input(
                label=f"Masukkan jumlah alternatif (Min: 2, Max: {max_alternatif_tersedia}):",
                min_value=2, max_value=max_alternatif_tersedia, value=min(3, max_alternatif_tersedia), step=1
            )
            
        st.write("---")

        # data kriteria
        semua_kriteria = [
            {"nama": "Salary (Gaji USD)", "kolom_csv": "Salary", "type": "benefit", "min": 0, "max": 200000, "default": 70000, "step": 5000},
            {"nama": "Skills Gap (Tingkat Kesulitan)", "kolom_csv": "Skills Gap", "type": "cost", "min": 1.0, "max": 10.0, "default": 5.0, "step": 0.1},
            {"nama": "Job Satisfaction (Kepuasan Kerja)", "kolom_csv": "Job Satisfaction", "type": "benefit", "min": 1, "max": 10, "default": 7, "step": 1},
            {"nama": "Work Life Balance (Keseimbangan Waktu)", "kolom_csv": "Work Life Balance", "type": "benefit", "min": 1, "max": 10, "default": 6, "step": 1},
            {"nama": "Growth Opportunity (Pertumbuhan Karir)", "kolom_csv": "Growth Opportunity", "type": "benefit", "min": 1, "max": 30, "default": 15, "step": 1},
            {"nama": "Edu Level (Tingkat Pendidikan)", "kolom_csv": "Edu Level", "type": "benefit", "min": 1, "max": 5, "default": 3, "step": 1},
        ]
        daftar_nama_kriteria = [k["nama"] for k in semua_kriteria]

        # selectbox kriteria sesuai dengan jumlah yang diinput
        st.subheader("📋 Pilih Kriteria")
        kriteria_terpilih = []
        
        # Looping untuk membuat selectbox sebanyak jumlah_kriteria
        for i in range(int(jumlah_kriteria)):
            # Set default index biar gak kembar pilihannya di awal loading
            default_idx = min(i, len(daftar_nama_kriteria) - 1)
            pilihan = st.selectbox(
                f"Kriteria Ke-{i+1}:", 
                options=daftar_nama_kriteria, 
                index=default_idx,
                key=f"sel_kri_{i}"
            )
            if pilihan not in kriteria_terpilih:
                kriteria_terpilih.append(pilihan)
            else:
                st.warning(f"⚠️ Kamu memilih kriteria **'{pilihan}'** lebih dari sekali! Silakan ganti kriteria yang unik.")

        st.write("---")

        # selectbox alternatif sesuai dengan jumlah yang diinput
        st.subheader("🏆 Pilih Alternatif Pekerjaan")
        alternatif_terpilih = []
        
        # Looping untuk membuat selectbox sebanyak jumlah_alternatif
        for j in range(int(jumlah_alternatif)):
            default_idx_alt = min(j, len(daftar_alternatif_riil) - 1)
            pilihan_alt = st.selectbox(
                f"Alternatif Pekerjaan Ke-{j+1}:", 
                options=daftar_alternatif_riil, 
                index=default_idx_alt,
                key=f"sel_alt_{j}"
            )
            if pilihan_alt not in alternatif_terpilih:
                alternatif_terpilih.append(pilihan_alt)
            else:
                st.warning(f"Kamu memilih alternatif **'{pilihan_alt}'** lebih dari sekali! Silakan pilih jenis pekerjaan yang berbeda.")

        st.write("---")

        # cek pilihan selectbox yang kembar/duplikat oleh user
        if len(kriteria_terpilih) != jumlah_kriteria or len(alternatif_terpilih) != jumlah_alternatif:
            st.error("Pastikan pilihan kriteria maupun alternatif unik (tidak ada yang double)!")
        else:
            # input nilai bobot fuzzy 
            st.subheader("📊 Isi Nilai Variabel Target Fuzzy")
            
            input_user_aktif = {}
            mapping_aktif = {}

            for kriteria in semua_kriteria:
                if kriteria["nama"] in kriteria_terpilih:
                    tanda = "🟢 Benefit" if kriteria["type"] == "benefit" else "🔴 Cost"
                    nilai_slider = st.slider(
                        label=f"{tanda} {kriteria['nama']}:",
                        min_value=kriteria["min"], max_value=kriteria["max"],
                        value=kriteria["default"],
                        step=kriteria["step"] if isinstance(kriteria["step"], float) else int(kriteria["step"])
                    )
                    input_user_aktif[kriteria['nama']] = nilai_slider
                    mapping_aktif[kriteria['nama']] = {
                        "kolom": kriteria["kolom_csv"],
                        "type": kriteria["type"],
                        "min": kriteria["min"],
                        "max": kriteria["max"]
                    }

            # Simpan data pilihan ke session state, digunakan di page Output
            st.session_state['input_user_aktif'] = input_user_aktif
            st.session_state['mapping_aktif'] = mapping_aktif
            st.session_state['alternatif_terpilih'] = alternatif_terpilih

            st.write("---")
            if st.button("🚀 Simpan data"):
                st.success("Data input berhasil disimpan! Silakan buka menu **Output** di sidebar untuk melihat hasil ranking.")
    else:
        st.error("File CSV dataset belum berhasil dimuat dengan benar.")


# OUTPUT
elif page == "Output" :
    st.write("lanjutin ya ji")