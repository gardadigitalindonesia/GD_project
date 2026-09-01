import streamlit as st

st.set_page_config(page_title="Materi 1", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 1: Pengenalan Social Engineering</h1>", unsafe_allow_html=True)
st.write("Penipu tidak selalu memecahkan password. Mereka sering memanfaatkan emosi seperti panik, rasa takut, dan rasa buru-buru untuk memaksa korban melakukan keputusan yang tidak aman.")
st.write("Contoh umum: seseorang mengirim pesan yang mengancam akun akan diblokir, lalu memaksa korban klik link dan membagikan kode OTP.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 1")
st.markdown("Anda menerima pesan WhatsApp yang mengatakan akun Anda akan dibekukan dalam 10 menit. Tindakan paling aman yang harus Anda lakukan adalah?")

opsi = [
    "Langsung mengecek ke kanal resmi bank atau marketplace, bukan link yang dikirim di chat.",
    "Segera masuk ke link karena pesan itu datang dari nomor yang mirip layanan resmi.",
    "Memberi tahu orang lain agar ikut mengecek akun.",
    "Mengirim kode OTP supaya akun bisa diselamatkan.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Verifikasi melalui kanal resmi adalah langkah paling aman.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Kembali"):
        st.switch_page("app9.py")
with col2:
    if st.button("➡️ Materi 2"):
        st.switch_page("pages/02_Materi_2.py")
