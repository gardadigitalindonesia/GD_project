import streamlit as st

st.set_page_config(page_title="Materi 14", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 14: Malware Kurir & File APK</h1>", unsafe_allow_html=True)
st.write("File APK yang dikirim melalui pesan instan sering kali dijebak sebagai versi resmi atau dokumen penting. Setelah diinstal, file itu bisa menyalin data dan merusak perangkat.")
st.write("Keuntungan jangka pendek tidak sebanding dengan risiko kehilangan data dan kontrol akun.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 14")
st.markdown("Anda menerima file APK yang dikirim dari kurir dengan alasan cek resi. Apa tindakan paling aman?")

opsi = [
    "Menolak instal dan mengecek status resi melalui aplikasi atau situs resmi ekspedisi.",
    "Langsung instal agar cepat selesai.",
    "Menyimpan file lalu membagikan ke teman.",
    "Meminta kurir untuk mengirim file tersebut kembali lewat email.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. File resmi dan aman selalu tersedia di aplikasi atau situs resmi, bukan file APK yang dikirim sembarangan.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 13"):
        st.switch_page("pages/13_Materi_13.py")
with col2:
    if st.button("➡️ Materi 15"):
        st.switch_page("pages/15_Materi_15.py")
