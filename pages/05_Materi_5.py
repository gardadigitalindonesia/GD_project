import streamlit as st

st.set_page_config(page_title="Materi 5", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 5: File APK Kurir & Tilang Palsu</h1>", unsafe_allow_html=True)
st.write("File APK atau aplikasi bajakan sering dikirim melalui WhatsApp dengan alasan resmi. Padahal file itu bisa mengumpulkan data, mengeksfiltrasi login, atau membajak akun.")
st.write("Kecepatan dan rasa ingin segera tahu membuat orang lebih mudah tertipu oleh file yang tampak sah.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 5")
st.markdown("Anda menerima file APK berisi surat tilang digital dan minta diinstal untuk melihat bukti. Tindakan tepat yang Anda pilih adalah?")

opsi = [
    "Menyimpan file lalu mengecek ke kanal resmi, bukan langsung instal.",
    "Segera membuka karena ada foto di dalamnya.",
    "Menginstal karena sudah dari pihak berwenang.",
    "Bagikan ke teman agar semua ikut periksa.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. File APK dari channel tidak resmi bisa berbahaya dan mencuri data sensitif.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 4"):
        st.switch_page("pages/04_Materi_4.py")
with col2:
    if st.button("➡️ Materi 6"):
        st.switch_page("pages/06_Materi_6.py")
