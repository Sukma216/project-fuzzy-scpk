import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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
    st.title("🧮 Perhitungan SPK Karir Dinamis (Fuzzy Mamdani)")
    st.write("Aplikasi ini mendukung pemilihan jumlah kriteria secara dinamis sesuai kebutuhan analisis kamu.")

    # Dropdown buat milih jurusan 
    jurusan_user = st.selectbox("🎯 Pilih Latar Belakang Jurusan Kamu:", list_jurusan)
    st.session_state['jurusan_user'] = jurusan_user

    st.write("---")

    # User input jumlah kriteria berupa angka
    st.subheader("⚙️ Pengaturan Kriteria")
    jumlah_kriteria = st.number_input(
        label="Masukkan jumlah kriteria yang ingin digunakan (Min: 2, Max: 6):",
        min_value=2, max_value=6, value=3, step=1
    )
    st.info(f"Target jumlah kriteria yang harus dipilih: **{jumlah_kriteria} Kriteria**.")

    # User memilih kriteria apa saja yang mau dipakai
    semua_kriteria = [
        {"nama": "Salary (Gaji USD)", "type": "benefit", "min": 0, "max": 200000, "default": 70000, "step": 5000},
        {"nama": "Skills Gap (Tingkat Kesulitan)", "type": "cost", "min": 1.0, "max": 10.0, "default": 5.0, "step": 0.1},
        {"nama": "Job Satisfaction (Kepuasan Kerja)", "type": "benefit", "min": 1, "max": 10, "default": 7, "step": 1},
        {"nama": "Work Life Balance (Keseimbangan Waktu)", "type": "benefit", "min": 1, "max": 10, "default": 6, "step": 1},
        {"nama": "Growth Opportunity (Pertumbuhan Karir)", "type": "benefit", "min": 1, "max": 30, "default": 15, "step": 1},
        {"nama": "Edu Level (Tingkat Pendidikan)", "type": "benefit", "min": 1, "max": 5, "default": 3, "step": 1},
    ]

    # ambil daftar semua nama kriteria
    daftar_nama_kriteria = [k["nama"] for k in semua_kriteria]

    # Multiselect kriteria dengan default mengambil sebanyak jumlah_kriteria pertama
    kriteria_terpilih = st.multiselect(
        label=f"Silakan pilih tepat {jumlah_kriteria} kriteria di bawah ini:",
        options=daftar_nama_kriteria,
        default=daftar_nama_kriteria[:jumlah_kriteria]
    )

    st.write("---")

    # buat cek apakah jumlah yang dicentang sudah pas dengan inputan angka di atas
    if len(kriteria_terpilih) != jumlah_kriteria:
        st.warning(f"⚠️ Jumlah kriteria yang dicentang ({len(kriteria_terpilih)}) belum sesuai dengan jumlah yang kamu input di atas ({jumlah_kriteria}).")
    else:
        st.subheader("📊 Isi Nilai Variabel Fuzzy")

        input_user_aktif = {}

        # looping hanya namppilin slider sesuai dengan jumlah kriteria dan kriteria apa aja yg diinput
        for kriteria in semua_kriteria:
            if kriteria["nama"] in kriteria_terpilih:
                tanda = "🟢 [Benefit]" if kriteria["type"] == "benefit" else "🔴 [Cost]"
                
                nilai_slider = st.slider(
                    label=f"{tanda} {kriteria['nama']}:",
                    min_value=kriteria["min"], max_value=kriteria["max"],
                    value=kriteria["default"],
                    step=kriteria["step"] if isinstance(kriteria["step"], float) else int(kriteria["step"])
                )
                input_user_aktif[kriteria['nama']] = nilai_slider

        st.session_state['input_user_aktif'] = input_user_aktif

        st.write("---")
        if st.button("🚀 Simpan Data"):
            st.success("Input kriteria berhasil disimpan! Silakan klik menu **Output** di sidebar untuk melihat hasil perhitungan Fuzzy Mamdani.")
            
            # nampilkan hasil kriteria dan bobot tersimpan yang diinput oleh User
            st.markdown("**Daftar Nilai Kriteria Tersimpan:**")
            for nama_kriteria, nilai in input_user_aktif.items():
                st.write(f"🔹 **{nama_kriteria}** : {nilai}")

# OUTPUT    
elif page == "Output" :
    st.title("Hasil Rekomendasi Pekerjaan (Fuzzy Mamdani)")
    
    if 'input_user_aktif' in st.session_state and 'jurusan_user' in st.session_state:
        input_data = st.session_state['input_user_aktif']
        jurusan = st.session_state['jurusan_user']
        
        st.write(f"Berikut adalah hasil rekomendasi karir berdasarkan preferensi kriteria untuk lulusan **{jurusan}**:")
        
        st.markdown("### 📋 Kriteria yang Dinilai:")
        for nama_kriteria, nilai in input_data.items():
            st.write(f"✅ **{nama_kriteria}** : {nilai}")
        
        st.write("---")
        st.warning("⚠️ Langkah Berikutnya: Masukkan fungsi mesin inferensi skfuzzy.control di sini untuk menghitung matriks 10 pekerjaan unik!")
        
    else:
        st.error("Kamu belum melakukan input preferensi kriteria. Silakan masuk ke menu **Input** terlebih dahulu.")