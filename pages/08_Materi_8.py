import streamlit as st

st.set_page_config(page_title="Materi 8", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 8: Suspensi Akun Toko & Merchant</h1>", unsafe_allow_html=True)
st.write("Penipu sering mengaku dari marketplace atau merchant platform dan menekan pelaku usaha untuk segera memverifikasi ulang agar akun tidak dibekukan.")
st.write("Situasi ini sangat berisiko karena banyak pelaku usaha sedang fokus pada operasional dan lebih rentan terhadap tekanan waktu.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 8")
st.markdown("Akun toko Anda menerima chat dari nomer yang tampak seperti admin marketplace: ‘Akun Anda akan dibekukan jika tidak verifikasi hari ini.’ Apa yang paling benar?")

opsi = [
    "Membuka aplikasi resmi marketplace dan mengecek status akun secara mandiri.",
    "Segera klik tautan yang dikirim chat.",
    "Memberikan kode OTP supaya akun dibuka kembali.",
    "Membalas dengan data rekening agar bisa diproses.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Kebenaran harus diverifikasi melalui aplikasi resmi, bukan tautan dari chat yang mengancam.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 7"):
        st.switch_page("pages/07_Materi_7.py")
with col2:
    if st.button("➡️ Materi 9"):
        st.switch_page("pages/09_Materi_9.py")
