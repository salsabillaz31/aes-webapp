import streamlit as st

st.set_page_config(page_title="AES WebApp", layout="wide")

# Cek apakah user sudah login
if "username" not in st.session_state:
    st.switch_page("pages/login.py")

# Redirect berdasarkan peran
if st.session_state["role"] == "dosen":
    st.switch_page("pages/dashboard_dosen.py")
elif st.session_state["role"] == "mahasiswa":
    st.switch_page("pages/dashboard_mahasiswa.py")
else:
    st.warning("Peran tidak dikenali.")
