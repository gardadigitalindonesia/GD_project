import streamlit as st

st.set_page_config(page_title="Materi 2", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 2: Ancaman Pembobolan Rekening & E-Wallet</h1>", unsafe_allow_html=True)
st.write("Pada pukul 00.30, Pak Budi menerima SMS yang berbunyi: ‘AKUN BANK ANDA DIBLOKIR. Verifikasi ulang dalam 2 jam untuk mencegah saldo hangus.’")
st.write("Teks itu terasa sangat menekan karena datang di tengah malam, tepat saat ia sedang memikirkan pembayaran karyawan dan biaya bahan baku.")
st.write("Ia tidak memeriksa apakah SMS itu benar-benar dikirim dari bank resmi. Ia langsung mengeklik tautan yang tertera.")
st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 2")
st.markdown("Anda menerima SMS dari nomor handphone biasa: ‘AKUN BANK ANDA DIBLOKIR. Untuk mengaktifkan kembali, silakan verifikasi data Anda di bca-validasi-data.com.’ Apa tindakan paling tepat?")

options = [
    "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.",
    "Menelepon tombol konfirmasi di SMS tersebut karena kemungkinan itu adalah komunikasi resmi dari bank.",
    "Mengirimkan kode OTP ke nomor lain agar bank bisa memverifikasi bahw a rekening Anda masih aktif.",
    "Segera membalas SMS dengan format yang sama agar penipu merasa dihormati dan tidak menghubungi lagi.",
]
selected = st.radio("Pilih jawaban paling tepat:", options, label_visibility="collapsed")

if selected:
    st.success("Jawaban yang aman adalah opsi pertama. Selalu cek melalui kanal resmi, bukan link yang dikirim lewat SMS.")

if st.button("⬅️ Kembali ke Aplikasi"):
    st.switch_page("app9.py")
