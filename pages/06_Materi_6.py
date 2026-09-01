import streamlit as st

st.set_page_config(page_title="Materi 6", page_icon="📘", layout="wide")

st.markdown("<h1 style='margin-top:0; font-size:2.2rem;'>📘 Materi 6: Pajak & Denda Palsu</h1>", unsafe_allow_html=True)
st.write("Penipu sering mengirim dokumen denda atau surat pajak palsu agar korban merasa terancam. Mereka berharap Anda segera membayar tanpa mengecek keaslian dokumen.")
st.write("Kunci utamanya adalah verifikasi melalui kanal resmi, bukan dokumen yang dikirim mendadak.")

st.markdown("---")
st.subheader("✍️ UJIAN MANDIRI MATERI 6")
st.markdown("Anda menerima surat pajak digital berisi denda besar dan meminta pembayaran via link yang disertakan. Apa tindakan paling tepat?")

opsi = [
    "Memverifikasi nomor resmi kantor pajak dan menghubungi mereka melalui kanal resmi.",
    "Membayar langsung karena denda dan surat itu terlihat formal.",
    "Mengirim data NPWP lewat chat untuk konfirmasi.",
    "Membagikan dokumen ke teman agar ikut mengecek.",
]
selected = st.radio("Pilih jawaban paling tepat:", opsi, label_visibility="collapsed")

if selected:
    st.success("Benar. Denda resmi selalu diverifikasi lewat kanal otoritas, bukan tautan yang dibagikan mendadak.")

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Materi 5"):
        st.switch_page("pages/05_Materi_5.py")
with col2:
    if st.button("➡️ Materi 7"):
        st.switch_page("pages/07_Materi_7.py")
