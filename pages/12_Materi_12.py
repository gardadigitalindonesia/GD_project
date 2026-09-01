import streamlit as st

st.set_page_config(page_title="Materi 12", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 12: Saham Palsu & File APK</h1>", unsafe_allow_html=True)
st.write("Penipu sering menyamar sebagai karyawan emiten atau tim investor, lalu mengirim file APK atau link investasi palsu. Mereka memakai istilah yang tampak sah untuk membangun rasa percaya.")
st.write("Yang penting adalah memeriksa validitas pihak yang mengirim dan membandingkan dengan kanal resmi perusahaan.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 12")
st.markdown("Anda mendapat file APK dari nomor yang mengaku karyawan emiten, berisi informasi pembagian dividen. Apa yang paling aman?")

opsi = [
    "Mengecek langsung ke investor relations atau website resmi emiten.",
    "Langsung instal file karena itu dari karyawan resmi.",
    "Memberi username dan password ke mereka.",
    "Membagikan file itu ke teman untuk diverifikasi.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Informasi resmi selalu tersedia di kanal perusahaan yang kredibel, bukan file tidak resmi yang dikirim di chat.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 11"):
        st.switch_page("pages/11_Materi_11.py")
with col2:
    if st.button("➡️ Materi 13"):
        st.switch_page("pages/13_Materi_13.py")
