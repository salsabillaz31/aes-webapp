import streamlit as st

st.write("Versi Streamlit:", st.__version__)

if st.button("Klik untuk rerun"):
    st.rerun()
