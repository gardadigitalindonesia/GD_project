import streamlit as st

st.set_page_config(page_title="Materi 11", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 11: Investasi Bodong</h1>", unsafe_allow_html=True)
st.write("Investasi bodong sangat sering menjanjikan hasil cepat dan menggiurkan. Penipu biasanya menekan cepat bertindak agar korban tidak mengecek legalitasnya.")
st.write("Saat tawaran terlalu bagus, langkah paling aman adalah berhenti sejenak dan verifikasi ke sumber resmi.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 11")
st.markdown("Anda diminta ikut grup Telegram yang menjanjikan hasil investasi luar biasa dalam 24 jam. Apa yang harus Anda lakukan?")

opsi = [
    "Memeriksa legalitas dan otoritas perusahaan serta mencari sumber resmi lain.",
    "Segera ikut karena hasilnya menjanjikan besar.",
    "Mengirim dana untuk ikut program tersebut.",
    "Menyebarkan peluang itu ke teman agar semuanya bisa untung.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Tawaran cepat dan sangat menguntungkan sering kali merupakan indikator investasi bodong.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 10"):
        st.switch_page("pages/10_Materi_10.py")
with col2:
    if st.button("➡️ Materi 12"):
        st.switch_page("pages/12_Materi_12.py")
