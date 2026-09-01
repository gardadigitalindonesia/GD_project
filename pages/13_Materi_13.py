import streamlit as st

st.set_page_config(page_title="Materi 13", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 13: Takeover Akun & OTP</h1>", unsafe_allow_html=True)
st.write("Penipu sering meminta kode OTP sebagai alasan untuk memverifikasi identitas, padahal tujuan sebenarnya adalah menguasai akun korban.")
st.write("Sebuah akun aman tidak pernah dibuka dengan memberikan kode OTP kepada siapapun.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 13")
st.markdown("Anda menerima telepon dari yang mengaku admin dan meminta kode OTP untuk memastikan keamanan akun. Apa yang paling aman?")

opsi = [
    "Menolak dan menghubungi layanan resmi melalui kanal yang sudah Anda kenal.",
    "Memberi kode tersebut agar akun segera aman.",
    "Menjawab supaya tidak dianggap mencurigakan.",
    "Menyimpan kode OTP untuk nanti diberikan jika diminta.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Kode OTP adalah kunci akses. Jangan pernah memberikannya ke siapa pun, termasuk yang mengaku resmi.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 12"):
        st.switch_page("pages/12_Materi_12.py")
with col2:
    if st.button("➡️ Materi 14"):
        st.switch_page("pages/14_Materi_14.py")
