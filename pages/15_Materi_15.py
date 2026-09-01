import streamlit as st

st.set_page_config(page_title="Materi 15", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 15: Struk Palsu & Bukti Transfer</h1>", unsafe_allow_html=True)
st.write("Struk atau bukti transfer palsu sering disusun dengan tampilan sangat meyakinkan. Tujuannya adalah menipu orang agar percaya dan bertindak tanpa verifikasi.")
st.write("Bukti yang sah harus dapat diverifikasi melalui sumber yang jelas dan resmi.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 15")
st.markdown("Anda menerima foto struk transfer yang tampak sangat profesional dari pembeli atau mitra, lalu diminta cepat membenarkan data. Apa tindakan paling aman?")

opsi = [
    "Memverifikasi melalui kanal resmi dan mengecek riwayat transaksi di sistem Anda.",
    "Langsung membenarkan data karena struk terlihat meyakinkan.",
    "Membagikan bukti ke semua staf agar cepat diselesaikan.",
    "Mengirim uang supaya tidak menimbulkan masalah.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Bukti valid harus dapat diverifikasi dari sistem internal atau sumber resmi.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 14"):
        st.switch_page("pages/14_Materi_14.py")
with col2:
    if st.button("➡️ Materi 16"):
        st.switch_page("pages/16_Materi_16.py")
