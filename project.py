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
    st.markdown("""
        <style>

        /* Style untuk Hero Section Container */
        .hero-container {
            background: linear-gradient(135deg, #1E3A8A 0%, #0D9488 100%);
            padding: 3.5rem 2rem;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 2.5rem;
            box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.3);
        }
        
        .hero-title {
            font-size: 40px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            margin-bottom: 10px;
            line-height: 1.2;
        }
        
        .hero-subtitle {
            font-size: 18px !important;
            color: #E2E8F0 !important;
            font-weight: 300;
            max-width: 600px;
            margin: 0 auto 25px auto;
        }
        
        /* Card Fitur / Keunggulan */
        .feature-card {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-left: 5px solid #0D9488;
            margin-bottom: 1rem;
            height: 100%;
        }
        
        .feature-title {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #1E3A8A;
            margin-bottom: 8px;
        }
        
        .feature-text {
            font-size: 14px;
            color: #4B5563;
            line-height: 1.5;
        }
        
        /* Stat/Badge Info */
        .stat-box {
            background-color: #EFF6FF;
            border: 1px solid #BFDBFE;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">🚀 Smart Career Pathfinder</h1>
            <p class="hero-subtitle">Temukan masa depan karir terbaikmu secara objektif menggunakan kecerdasan sistem pendukung keputusan berbasis Logika Fuzzy Mamdani.</p>
        </div>
    """, unsafe_allow_html=True)

    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
        st.markdown("""
            <div class="stat-box">
                <h3 style='margin:0; color:#1E3A8A;'>🧠 Fuzzy Logik</h3>
                <p style='margin:0; font-size:14px; color:#4B5563;'>Mamdani Implication</p>
            </div>
        """, unsafe_allow_html=True)
    with col_stat2:
        st.markdown("""
            <div class="stat-box">
                <h3 style='margin:0; color:#0D9488;'>📊 Data Driven</h3>
                <p style='margin:0; font-size:14px; color:#4B5563;'>Kalkulasi Riil Dataset</p>
            </div>
        """, unsafe_allow_html=True)
    with col_stat3:
        st.markdown("""
            <div class="stat-box">
                <h3 style='margin:0; color:#8B5CF6;'>🎯 Personalisasi</h3>
                <p style='margin:0; font-size:14px; color:#4B5563;'>Sesuai Preferensimu</p>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")
    st.markdown("<h3 style='text-align: center; color: #1E3A8A; margin-bottom: 1.5rem;'>🛠️ Tiga Langkah Mudah Memulai Analisis</h3>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">1. Pilih Alternatif</div>
                <div class="feature-text">Tentukan jurusan asalmu serta pilih beberapa alternatif pekerjaan yang ingin kamu komparasikan kecocokannya.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_f2:
        st.markdown("""
            <div class="feature-card" style="border-left-color: #1E3A8A;">
                <div class="feature-title">2. Atur Preferensi</div>
                <div class="feature-text">Gunakan slider interaktif untuk memasukkan target idealmu pada kriteria Gaji, Work-Life Balance, hingga Skills Gap.</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col_f3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">3. Lihat Rekomendasi</div>
                <div class="feature-text">Sistem akan melakukan proses fuzzifikasi, evaluasi aturan, dan memberikan laporan perangkingan lengkap berupa grafik.</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

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
            {"nama": "Work Life Balance (Keseimbangan Waktu)", "kolom_csv": "Work-Life Balance", "type": "benefit", "min": 1, "max": 10, "default": 6, "step": 1},
            {"nama": "Growth Opportunity (Pertumbuhan Karir)", "kolom_csv": "Industry Growth Rate", "type": "benefit", "min": 1, "max": 30, "default": 15, "step": 1},
            {"nama": "Edu Level (Tingkat Pendidikan)", "kolom_csv": "Education Level", "type": "benefit", "min": 1, "max": 5, "default": 3, "step": 1},
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


elif page == "Output":
    st.title("📈 Hasil Rekomendasi Pekerjaan")
    st.write("Berikut hasil perhitungan untuk pendukung keputusan berdasarkan data yang sudah kamu input sebelumnya.")

    if (
        'input_user_aktif' not in st.session_state or
        'mapping_aktif' not in st.session_state or
        'alternatif_terpilih' not in st.session_state or
        'jurusan_user' not in st.session_state
    ):
        st.warning("⚠️ Silakan isi data terlebih dahulu pada menu Input.")

    else:
        # Ambil data dari session state
        input_user = st.session_state['input_user_aktif']
        mapping_aktif = st.session_state['mapping_aktif']
        alternatif_terpilih = st.session_state['alternatif_terpilih']
        jurusan_user = st.session_state['jurusan_user']

        # informasi data yang diinput user
        st.subheader("🎓 Informasi Pengguna")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Jurusan Dipilih: **{jurusan_user}**")
        with col2:
            st.success(f"Jumlah Alternatif: **{len(alternatif_terpilih)}**")
        st.write("---")

        # data prepocessing
        df_hasil = df_asli[
            (df_asli['Field of Study'] == jurusan_user) &
            (df_asli['Current Occupation'].isin(alternatif_terpilih))
        ].copy()
        
        if df_hasil.empty:
            st.error("❌ Data tidak ditemukan untuk kombinasi alternatif ini di dataset asli.")
            st.stop()

        # ambil kolom csv dari mapping aktif
        kolom_dari_mapping = []
        for info_kriteria in mapping_aktif.values():
            if 'kolom' in info_kriteria:
                kolom_dari_mapping.append(info_kriteria['kolom'])

        kolom_numerik_otomatis = []
        kolom_yang_hilang = []

        for col in kolom_dari_mapping:
            if col in df_hasil.columns:
                kolom_numerik_otomatis.append(col)
            else:
                kolom_yang_hilang.append(col)

        # kalo ada kolom yang salah ketik, ada tampilan peringatan di Streamlit
            st.warning(f"⚠️ **Peringatan Struktur CSV:** Kolom {kolom_yang_hilang} tidak ditemukan di file CSV. Pastikan penulisan di `mapping_aktif` sudah sama persis.")

        # kalo tidak ada satu pun kriteria yang cocok dengan CSV, hentikan agar tidak crash
        if not kolom_numerik_otomatis:
            st.error("❌ Tidak ada kolom kriteria yang cocok dengan dataset. Periksa kembali file konfigurasi mapping kamu!")
            st.stop()

        # Konversi kategori khusus ke numerik (Hanya jika kolomnya ada di dataset)
        if "Industry Growth Rate" in df_hasil.columns:
            df_hasil["Industry Growth Rate"] = df_hasil["Industry Growth Rate"].astype(str).str.strip().str.lower()
            df_hasil["Industry Growth Rate"] = df_hasil["Industry Growth Rate"].replace({"low": 10, "medium": 20, "high": 30})
        
        if "Education Level" in df_hasil.columns:
            df_hasil["Education Level"] = df_hasil["Education Level"].astype(str).str.strip().str.lower()
            df_hasil["Education Level"] = df_hasil["Education Level"].replace({"high school": 1, "associate": 2, "bachelor": 3, "master": 4, "phd": 5})
        
        # Paksa semua kolom kriteria yang valid menjadi tipe data numerik
        for col in kolom_numerik_otomatis:
            df_hasil[col] = pd.to_numeric(df_hasil[col], errors='coerce')

        # Hitung rata-rata berdasarkan kriteria yang VALID aja
        kolom_numerik_otomatis = list(set(kolom_numerik_otomatis))
        
        hasil_group = df_hasil.groupby('Current Occupation')[kolom_numerik_otomatis].mean()
        hasil_group.columns = hasil_group.columns.str.strip()

        # visualisasi fungsi keanggotaan
        st.subheader(" 1. Analisis Fungsi Keanggotaan Per Kriteria")
        st.write("Di bawah ini adalah analisis kurva fuzzy untuk masing-masing kriteria. Garis hitam tegas merupakan nilai target yang kamu tentukan, sedangkan garis putus-putus adalah posisi nilai rata-rata dari dataset:")

        warna_garis = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 'gray']

        # Looping untuk menggambar grafik kriteria satu per satu secara berurutan
        for nama_kriteria, nilai_user in input_user.items():
            kolom_csv = mapping_aktif[nama_kriteria]['kolom']
            nilai_min = mapping_aktif[nama_kriteria]['min']
            nilai_max = mapping_aktif[nama_kriteria]['max']

            if kolom_csv not in hasil_group.columns:
                continue

            # Bangun range Semesta Pembicaraan (X)
            x_range = np.arange(nilai_min, nilai_max + 1, 1)

            # Buat kurva keanggotaan Segitiga (Trimf)
            rendah = fuzz.trimf(x_range, [nilai_min, nilai_min, (nilai_min + nilai_max)/2])
            sedang = fuzz.trimf(x_range, [nilai_min, (nilai_min + nilai_max)/2, nilai_max])
            tinggi = fuzz.trimf(x_range, [(nilai_min + nilai_max)/2, nilai_max, nilai_max])

            # Mulai plotting grafik kriteria ini
            fig_kri, ax_kri = plt.subplots(figsize=(9, 4.5))
            ax_kri.plot(x_range, rendah, label='Rendah', linewidth=2.5)
            ax_kri.plot(x_range, sedang, label='Sedang', linewidth=2.5)
            ax_kri.plot(x_range, tinggi, label='Tinggi', linewidth=2.5)

            # Plot garis putus-putus untuk nilai pekerjaan/alternatif yang ada di dataset
            for idx_alt, pekerjaan in enumerate(alternatif_terpilih):
                if pekerjaan in hasil_group.index:
                    nilai_alt = hasil_group.loc[pekerjaan, kolom_csv]
                    if not pd.isna(nilai_alt):
                        ax_kri.axvline(
                            x=nilai_alt,
                            color=warna_garis[idx_alt % len(warna_garis)],
                            linestyle='--',
                            linewidth=1.8,
                            alpha=0.8,
                            label=f"Data: {pekerjaan}"
                        )

            # Plot garis hitam tegas sebagai Target yang diinput oleh User via Slider
            ax_kri.axvline(x=nilai_user, color='black', linestyle='-', linewidth=4, label='🎯 Target Kamu')

            # Atur kelengkapan dekorasi grafik
            ax_kri.set_title(f"Kurva Keanggotaan Kriteria: {nama_kriteria}", fontsize=12, fontweight='bold')
            ax_kri.set_xlabel("Nilai Numerik")
            ax_kri.set_ylabel("Derajat Keanggotaan (μ)")
            ax_kri.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=9)
            ax_kri.grid(True, alpha=0.3)

            # tampilan grafik
            st.markdown(f"#### 📊 Kurva Fuzzy Kriteria: {nama_kriteria}")
            st.pyplot(fig_kri)
            st.caption(f"Target ideal yang kamu tentukan pada kriteria **{nama_kriteria}** adalah sebesar **{nilai_user}**.")
            st.write("") # Memberi space antar grafik agar rapi

        st.write("---")

        # FUZZY MAMDANI
        skor_final = []
        for pekerjaan in alternatif_terpilih:
            if pekerjaan not in hasil_group.index:
                continue

            total_skor = 0
            jumlah_kriteria = 0

            for nama_kriteria, nilai_user in input_user.items():
                kolom_csv = mapping_aktif[nama_kriteria]['kolom']
                tipe = mapping_aktif[nama_kriteria]['type']
                nilai_min = mapping_aktif[nama_kriteria]['min']
                nilai_max = mapping_aktif[nama_kriteria]['max']

                if kolom_csv not in hasil_group.columns:
                    continue

                nilai_data = hasil_group.loc[pekerjaan, kolom_csv]
                if pd.isna(nilai_data):
                    continue

                x_range = np.arange(nilai_min, nilai_max + 1, 1)

                rendah = fuzz.trimf(x_range, [nilai_min, nilai_min, (nilai_min + nilai_max)/2])
                sedang = fuzz.trimf(x_range, [nilai_min, (nilai_min + nilai_max)/2, nilai_max])
                tinggi = fuzz.trimf(x_range, [(nilai_min + nilai_max)/2, nilai_max, nilai_max])

                # Fuzzifikasi input user
                user_rendah = fuzz.interp_membership(x_range, rendah, nilai_user)
                user_sedang = fuzz.interp_membership(x_range, sedang, nilai_user)
                user_tinggi = fuzz.interp_membership(x_range, tinggi, nilai_user)

                # Fuzzifikasi nilai data lapangan
                data_rendah = fuzz.interp_membership(x_range, rendah, nilai_data)
                data_sedang = fuzz.interp_membership(x_range, sedang, nilai_data)
                data_tinggi = fuzz.interp_membership(x_range, tinggi, nilai_data)

                # RULE BASE 
                rule1 = min(user_rendah, data_rendah)
                rule2 = min(user_sedang, data_sedang)
                rule3 = min(user_tinggi, data_tinggi)

                # AGREGASI ATURAN (MAX)
                agregasi = max(rule1, rule2, rule3)

                # IMPLEMENTASI COST / BENEFIT
                if tipe == "cost":
                    agregasi = 1 - agregasi

                # DEFUZZIFIKASI  (SKOR SKALA 100)
                skor = agregasi * 100
                total_skor += skor
                jumlah_kriteria += 1

            if jumlah_kriteria > 0:
                skor_akhir = total_skor / jumlah_kriteria
                skor_final.append({
                    "Pekerjaan": pekerjaan,
                    "Skor Kecocokan": round(skor_akhir, 2)
                })

        # susun ranking dataframe
        df_ranking = pd.DataFrame(skor_final)
        if df_ranking.empty:
            st.error("❌ Gagal memproses perangkingan fuzzy.")
            st.stop()

        df_ranking = df_ranking.sort_values(by="Skor Kecocokan", ascending=False).reset_index(drop=True)
        df_ranking.index = df_ranking.index + 1

        # OUTPUT, KESIMPULAN DAN REKOMENDASI
        st.subheader("📊 2. Hasil Keputusan Akhir Rekomendasi")
        
        pekerjaan_terbaik = df_ranking.iloc[0]['Pekerjaan']
        skor_terbaik = df_ranking.iloc[0]['Skor Kecocokan']

        st.success(f"""
         🎯 {pekerjaan_terbaik}
        dengan akumulasi derajat tingkat kecocokan sebesar **{skor_terbaik:.2f}%**.
        """)
        st.write("---")

        # TABEL PERANGKINGAN
        st.markdown("**📋 Tabel Urutan Ranking Alternatif:**")
        st.dataframe(df_ranking, use_container_width=True)
        st.write("---")

        # VISUALISASI PERANGKINGAN (BAR CHART)
        st.markdown("**📊 Grafik Batang Tingkat Kesesuaian:**")
        fig_bar, ax_bar = plt.subplots(figsize=(10, 4.5))
        bars = ax_bar.bar(df_ranking['Pekerjaan'], df_ranking['Skor Kecocokan'], color='skyblue', edgecolor='royalblue')
        ax_bar.set_title("Perbandingan Skor Kecocokan Hasil Rekomendasi", fontsize=12, fontweight='bold')
        ax_bar.set_xlabel("Alternatif Pekerjaan")
        ax_bar.set_ylabel("Skor Persentase (%)")
        ax_bar.set_ylim(0, 110)
        plt.xticks(rotation=15)

        for bar in bars:
            height = bar.get_height()
            ax_bar.text(
                bar.get_x() + bar.get_width()/2,
                height + 1,
                f'{height:.1f}%',
                ha='center',
                va='bottom',
                fontsize=9,
                fontweight='bold'
            )
        st.pyplot(fig_bar)
        st.write("---")
