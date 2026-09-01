import streamlit as st

st.set_page_config(page_title="Materi 20", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 20: Kesadaran Keamanan Digital</h1>", unsafe_allow_html=True)
st.write("Kesadaran keamanan digital bukan hanya soal keterampilan teknis, tapi juga kebiasaan berpikir. Saat ada permintaan mendesak, panik, atau menguntungkan, otak sering menangkap signal yang salah.")
st.write("Yang paling aman adalah menghentikan sejenak, memverifikasi, dan baru mengambil keputusan.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 20")
st.markdown("Anda mendapat tawaran cepat, menguntungkan, dan sangat mendesak. Apa sikap paling aman?")

opsi = [
    "Berhenti sejenak, verifikasi sumber, dan tidak langsung bertindak.",
    "Segera ikut karena ada tekanan waktu.",
    "Langsung mengirim dana atau data untuk menghindari kerugian.",
    "Menyebarkan tawaran itu ke semua orang agar mereka ikut cepat.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Keamanan digital dibangun dari ketenangan, verifikasi, dan keputusan yang tidak didorong oleh panik atau rasa takut.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 19"):
        st.switch_page("pages/19_Materi_19.py")
with col2:
    if st.button("🏠 Kembali ke Beranda"):
        st.switch_page("app9.py")
