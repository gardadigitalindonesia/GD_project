import streamlit as st

st.set_page_config(page_title="Materi 16", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 16: Verifikasi Dua Langkah (2FA)</h1>", unsafe_allow_html=True)
st.write("Aktivasi 2FA adalah salah satu pengaman terbaik untuk menghambat peretas. Namun, banyak korban justru menyerahkan kode OTP karena merasa sedang dalam situasi darurat.")
st.write("Pengaman yang benar tidak perlu diserahkan ke siapapun.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 16")
st.markdown("Anda menerima permintaan untuk memasukkan kode OTP demi ‘aktivasi keamanan’ dari nomor yang mengaku tim IT. Apa yang paling aman?")

opsi = [
    "Menolak dan mengecek apakah itu benar-benar merupakan kebutuhan dari tim IT resmi Anda.",
    "Memberi kode OTP agar proses aman.",
    "Mencatat kode dengan alasan bisa dipakai nanti.",
    "Membagikan kode ke rekan kerja agar semua ikut ikut.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. 2FA adalah pengaman, bukan sesuatu yang harus dibagikan terhadap permintaan yang tidak jelas.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 15"):
        st.switch_page("pages/15_Materi_15.py")
with col2:
    if st.button("➡️ Materi 17"):
        st.switch_page("pages/17_Materi_17.py")
