import streamlit as st

st.set_page_config(page_title="Materi 3", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 3: Fake CS WhatsApp</h1>", unsafe_allow_html=True)
st.write("Penipu sering menyamar sebagai customer service atau admin resmi dengan foto profil seperti benar-benar milik perusahaan.")
st.write("Mereka meminta data login, kode OTP, atau bahkan meminta korban mengunduh file untuk mempercepat proses.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 3")
st.markdown("Anda mendapat pesan dari akun WhatsApp yang tampak seperti customer service resmi, meminta Anda login ulang ke halaman verifikasi. Apa tindakan paling aman?")

opsi = [
    "Memeriksa nomor resmi perusahaan dan menghubungi mereka lewat kanal yang sudah dikenal.",
    "Langsung login karena akun tersebut tampak profesional.",
    "Mengirim OTP ke mereka agar akun aman.",
    "Mengisi data login agar proses cepat selesai.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. CS resmi tidak pernah meminta kode OTP atau password lewat chat pribadi.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 2"):
        st.switch_page("pages/02_Materi_2.py")
with col2:
    if st.button("➡️ Materi 4"):
        st.switch_page("pages/04_Materi_4.py")
