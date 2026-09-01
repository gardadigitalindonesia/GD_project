import streamlit as st

st.set_page_config(page_title="Materi 10", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 10: Bansos Palsu</h1>", unsafe_allow_html=True)
st.write("Penipu menggunakan narasi bantuan sosial atau hibah untuk membuat korban klik tautan dan menyerahkan data akun. Sering kali tawaran itu dibuat sangat menggiurkan.")
st.write("Keputusan aman adalah tidak langsung menanggapi tawaran yang datang lewat link asing atau chat pribadi.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 10")
st.markdown("Anda menerima pesan: ‘Dana hibah Rp5 juta siap cair, klik link untuk cek penerima.’ Tindakan paling aman adalah?")

opsi = [
    "Melalui kanal resmi pemerintah atau organisasi terkait sebelum percaya.",
    "Segera klik link untuk menyelesaikan proses cepat.",
    "Mengisi data pribadi agar bisa menerima bantuan.",
    "Membagikan link ke semua teman dekat.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Program bantuan resmi tidak pernah meminta data sensitif melalui link chat yang tampak mendadak.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 9"):
        st.switch_page("pages/09_Materi_9.py")
with col2:
    if st.button("➡️ Materi 11"):
        st.switch_page("pages/11_Materi_11.py")
