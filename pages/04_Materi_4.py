import streamlit as st

st.set_page_config(page_title="Materi 4", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 4: Vishing & Penipuan Telepon</h1>", unsafe_allow_html=True)
st.write("Vishing adalah teknik menipu melalui telepon atau panggilan suara. Pelaku mengaku dari bank, polisi, atau instansi resmi untuk menekan korban agar memberi data pribadi.")
st.write("Salah satu cirinya adalah ancaman keras dan permintaan cepat tanpa memberi waktu berpikir.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 4")
st.markdown("Telepon datang dengan suara yang terdengar seperti polisi: ‘Anda terlibat kasus dan harus segera transfer dana agar aman.’ Apa yang paling tepat Anda lakukan?")

opsi = [
    "Menghentikan panggilan dan menelpon nomor resmi instansi yang bersangkutan untuk verifikasi.",
    "Segera transfer dana karena ada ancaman hukum.",
    "Memberi kode OTP agar kasus bisa selesai.",
    "Mencatat semua informasi lalu dibagikan ke teman.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Verifikasi melalui kanal resmi menghindarkan Anda dari tekanan dan penipuan.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 3"):
        st.switch_page("pages/03_Materi_3.py")
with col2:
    if st.button("➡️ Materi 5"):
        st.switch_page("pages/05_Materi_5.py")
