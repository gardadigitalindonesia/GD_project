import streamlit as st

st.set_page_config(page_title="Materi 7", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 7: Surat Panggilan Sidang Palsu</h1>", unsafe_allow_html=True)
st.write("Penipu sering menyamar sebagai pihak hukum dan mengirim file APK atau surat pemanggilan yang terdengar resmi. Tujuannya adalah membuat korban panik dan langsung bertindak tanpa berpikir.")
st.write("Kuncinya: jangan menilai validitas dokumen hanya dari kesan formalnya.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 7")
st.markdown("Anda menerima surat sidang dengan nama instansi yang mirip, lengkap dengan logo dan nomor dokumen. Apa paling aman?")

opsi = [
    "Memastikan keaslian melalui kantor resmi dan nomor yang benar-benar dikenal.",
    "Membuka file untuk melihat detailnya.",
    "Membalas surat lalu memasukkan data pribadi.",
    "Langsung mengikuti tuntutan tanpa konfirmasi.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Panggilan resmi selalu bisa diverifikasi melalui kanal yang benar, bukan lewat file atau pesan mendadak.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 6"):
        st.switch_page("pages/06_Materi_6.py")
with col2:
    if st.button("➡️ Materi 8"):
        st.switch_page("pages/08_Materi_8.py")
