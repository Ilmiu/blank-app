import streamlit as st
import streamlit as st
import pandas as pd

# Database sederhana
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=['Tanggal', 'Nama', 'Jenis Sampah', 'Berat', 'Poin'])

st.title("♻️ Bank Sampah Digital")

# Input transaksi
with st.form("input_form"):
    nama = st.text_input("Nama Nasabah")
    jenis = st.selectbox("Jenis Sampah", ["Plastik", "Kertas", "Logam", "Organik"])
    berat = st.number_input("Berat (kg)", min_value=0.1)
    submitted = st.form_submit_button("Simpan")
    
    if submitted:
        poin = berat * {"Plastik":10, "Kertas":5, "Logam":15, "Organik":3}[jenis]
        new_data = pd.DataFrame([[pd.Timestamp.now(), nama, jenis, berat, poin]], 
                               columns=st.session_state.transactions.columns)
        st.session_state.transactions = pd.concat([st.session_state.transactions, new_data])
        st.success("Transaksi tersimpan!")

# Dashboard
st.subheader("Statistik")
col1, col2, col3 = st.columns(3)
col1.metric("Total Nasabah", st.session_state.transactions['Nama'].nunique())
col2.metric("Total Sampah (kg)", st.session_state.transactions['Berat'].sum())
col3.metric("Total Poin", st.session_state.transactions['Poin'].sum())

# Leaderboard
st.subheader("Top Nasabah")
top_users = st.session_state.transactions.groupby('Nama')['Poin'].sum().nlargest(5)
st.bar_chart(top_users)

# Tabel data
st.dataframe(st.session_state.transactions.sort_values('Tanggal', ascending=False))
