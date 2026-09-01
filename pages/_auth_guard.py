import streamlit as st


def require_login():
    if "login_sukses" not in st.session_state or not st.session_state.get("login_sukses"):
        st.warning("Silakan masuk ke aplikasi terlebih dahulu.")
        if st.button("⬅️ Kembali ke halaman masuk"):
            st.switch_page("app9.py")
        st.stop()
