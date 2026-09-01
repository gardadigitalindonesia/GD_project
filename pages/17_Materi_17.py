import streamlit as st

st.set_page_config(page_title="Materi 17", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 17: Email Phishing</h1>", unsafe_allow_html=True)
st.write("Email phishing sering menyamar ke akun resmi dan menarik korban untuk mengklik tautan atau mengunduh lampiran. Tujuannya adalah mengambil data sensitif atau menginfeksi perangkat.")
st.write("Kunci utamanya adalah memastikan sumber email yang benar-benar valid sebelum bertindak.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 17")
st.markdown("Anda menerima email dari alamat mirip supplier yang meminta update rekening via link. Apa terbaik yang Anda lakukan?")

opsi = [
    "Menghubungi supplier melalui nomor resmi yang sudah diketahui dan menanyakan kejelasan email.",
    "Klik link karena mengirim dari domain hampir sama.",
    "Mengirim password melalui email untuk validasi.",
    "Membuka lampiran agar bisa mengeceknya.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Email penting selalu diverifikasi dengan nomor atau kanal resmi, bukan melalui tautan yang dikirim pesan email.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 16"):
        st.switch_page("pages/16_Materi_16.py")
with col2:
    if st.button("➡️ Materi 18"):
        st.switch_page("pages/18_Materi_18.py")
