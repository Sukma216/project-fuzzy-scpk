import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.sidebar.title("Projek Akhir SCPK")
st.sidebar.header("About Us")
with st.sidebar.expander("Kelompok 7"):
    st.write("Nama : Dzahabia S Anjani")
    st.write("NIM : 123240037")
    st.write("Nama : Sukmawati Kharisma Gati")
    st.write("NIM : 123240137")
st.sidebar.markdown("---")
aslab = st.sidebar.selectbox(
    "Pilih salah satu",
    ["Home", "Data", "Input", "Output"]
)
st.sidebar.header("""📬 Contact Us

📧 Email: sukma@email.com  
📱 WhatsApp: 08xxxxxxxxxx  
🏫 UPN Veteran Yogyakarta  
""")