import streamlit as st

st.set_page_config(page_title="Materi 18", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 18: Pretext Calling</h1>", unsafe_allow_html=True)
st.write("Pretext calling dilakukan dengan menyamar sebagai pihak yang tampak berwenang. Tujuannya adalah membuat korban percaya dan mengungkapkan data atau melakukan aksi di luar kendali.")
st.write("Perhatian harus fokus pada identitas penelpon dan verifikasi silang sebelum memberikan data apa pun.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 18")
st.markdown("Anda ditelepon oleh orang yang mengaku dari bank dan meminta kode OTP untuk mengamankan rekening. Apa yang paling tepat?")

opsi = [
    "Menolak dan memanggil nomor resmi bank yang sudah dfiketahui untuk verifikasi.",
    "Memberi kode OTP karena orang itu mengaku dari bank.",
    "Menyampaikan data pribadi agar urusan cepat selesai.",
    "Memberi tahu seluruh staf tentang telepon itu agar semua ikut waspada.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Telepon atau chat yang menekan harus diverifikasi lewat nomor resmi, bukan nomor yang baru saja ditelpon.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 17"):
        st.switch_page("pages/17_Materi_17.py")
with col2:
    if st.button("➡️ Materi 19"):
        st.switch_page("pages/19_Materi_19.py")
