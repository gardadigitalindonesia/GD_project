import streamlit as st

st.set_page_config(page_title="Materi 9", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 9: Hoaks Rush Dollar</h1>", unsafe_allow_html=True)
st.write("Berita hoaks yang memicu kepanikan sering menyerukan aksi cepat, seperti menarik uang tunai atau mengikuti instruksi sehingga muncul rasa takut yang besar.")
st.write("Dalam situasi seperti ini, keputusan yang sehat adalah menahan diri dan mengecek kebenaran dari sumber resmi.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 9")
st.markdown("Anda mendapat informasi berantai bahwa uang tunai akan dibekukan dan nasabah harus segera menarik saldo. Apa tindakan paling bijak?")

opsi = [
    "Mengecek situs resmi bank atau lembaga terkait sebelum bertindak.",
    "Segera menarik saldo sesuai isi pesan.",
    "Menyebarkan informasi itu ke seluruh grup.",
    "Menghubungi nomor asing yang disebutkan di pesan.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Hoaks sering memanfaatkan rasa panik. Verifikasi terlebih dahulu lewat sumber resmi.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 8"):
        st.switch_page("pages/08_Materi_8.py")
with col2:
    if st.button("➡️ Materi 10"):
        st.switch_page("pages/10_Materi_10.py")
