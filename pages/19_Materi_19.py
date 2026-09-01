import streamlit as st

st.set_page_config(page_title="Materi 19", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 19: Impersonation Media Sosial</h1>", unsafe_allow_html=True)
st.write("Akun palsu di WhatsApp atau media sosial sering meniru orang atau perusahaan resmi. Mereka memanfaatkan kepercayaan dan reputasi untuk meminta data atau uang.")
st.write("Identitas online harus selalu diverifikasi dengan bukti yang konsisten, bukan sekadar tampilan profil yang meyakinkan.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 19")
st.markdown("Anda menerima DM dari akun yang tampak mirip admin perusahaan yang meminta dana darurat hari itu juga. Apa paling aman?")

opsi = [
    "Mengonfirmasi langsung ke nomor atau akun resmi yang sudah diketahui.",
    "Langsung mentransfer dana karena akun itu terkesan resmi.",
    "Menyebutkan data pribadi untuk verifikasi.",
    "Mengirimkan uang agar tidak mengecewakan.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Identitas digital harus diverifikasi silang sebelum ada transfer atau data sensitif.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 18"):
        st.switch_page("pages/18_Materi_18.py")
with col2:
    if st.button("➡️ Materi 20"):
        st.switch_page("pages/20_Materi_20.py")
