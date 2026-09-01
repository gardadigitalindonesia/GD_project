import streamlit as st
import matplotlib.pyplot as plt

# 1. Pengaturan Tampilan Halaman Web
st.set_page_config(page_title="GardaDigital", page_icon="🛡️", layout="centered")

# =========================================================================
# 🧠 SISTEM LOCKING DAN PENYIMPANAN SKOR (SESSION STATE)
# =========================================================================
if "skor_aman" not in st.session_state:
    st.session_state.skor_aman = 0
if "skor_bahaya" not in st.session_state:
    st.session_state.skor_bahaya = 0
if "materi_selesai" not in st.session_state:
    st.session_state.materi_selesai = set()

# Fungsi untuk mengunci jawaban per materi agar tidak bisa diubah
def kunci_jawaban(materi_id, jawaban_user, jawaban_benar):
    if materi_id not in st.session_state.materi_selesai:
        st.session_state.materi_selesai.add(materi_id)
        if jawaban_user == jawaban_benar:
            st.session_state.skor_aman += 1
        else:
            st.session_state.skor_bahaya += 1

# =========================================================================
# 🧭 STRUKTUR SIDEBAR BERTINGKAT (MODUL -> MATERI)
# =========================================================================
st.sidebar.title("🛡️ Panel Navigasi")

# Dropdown 1: Pemilihan Modul Utama
modul_terpilih = st.sidebar.selectbox(
    "Pilih Modul Pelatihan:",
    [
        "Modul 1: Social Engineering (Gratis)",
        "Modul 2: Digital Phishing & Link Palsu (🔒 Premium)",
        "Modul 3: Mengunci Brankas & Aset Bisnis (🔒 Premium)",
        "Modul 4: Sertifikasi & Manajemen Krisis (🔒 Premium)"
    ]
)

# Teks pilihan materi dikunci dalam variabel agar 100% sama dan tidak typo
m0 = "[ Baca Beranda Utama & Moto ]"
m1 = "Materi 1: Pengenalan Social Engineering"
m2 = "Materi 2: Ancaman Pemblokiran Rekening"
m3 = "Materi 3: Fake CS (Centang Hijau Palsu)"
m4 = "Materi 4: Vishing (Telepon Polisi Palsu)"
m_rapor = "📊 Rapor Hasil Evaluasi Saya"

# Dropdown 2: Pemilihan Materi secara Dinamis berdasarkan Modul 1
if "Modul 1" in modul_terpilih:
    menu = st.sidebar.selectbox(
        "Pilih Pembelajaran:",
        [m0, m1, m2, m3, m4, m_rapor]
    )
else:
    menu = "[ Terkunci 🔒 ]"
    st.sidebar.warning("🔒 Modul ini hanya bisa diakses oleh member Premium seharga Rp 50.000.")

# =========================================================================
# 🏛️ KONTEN HALAMAN TENGAH BERDASARKAN PILIHAN NAVIGASI
# =========================================================================

# ----------------- HALAMAN BERANDA / LOGO UTAMA -----------------
if menu == m0:
    st.write("") 
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-top: 0px;'>GardaDigital</h1>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #BDC3C7;'>\"Membangun Perisai Siber Akal Sehat, Melindungi Aset Toko & Rekening Tabungan Anda.\"</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.write("👋 **Selamat Datang di Platform Sertifikasi Keamanan Digital Mandiri GardaDigital.**")
    st.write("Sistem ini dirancang khusus untuk membantu pemilik bisnis, pelaku UMKM, dan personal dalam mendeteksi dan menggagalkan berbagai modus kejahatan siber yang marak di Indonesia.")
    st.info("👈 **Langkah Pertama:** Silakan buka menu di panel samping (*sidebar*) untuk memilih materi pembelajaran dari **Modul 1** dan mulailah menguji insting pertahanan digital Anda!")

# ----------------- KONTEN JIKA MODUL PREMIUM DIKLIK -----------------
elif menu == "[ Terkunci 🔒 ]":
    st.markdown(f"### 🔒 Akses Terkunci: {modul_terpilih}")
    st.error("Maaf, modul ini masuk ke dalam paket materi lanjutan (Premium member).")
    st.write("Tingkatkan pertahanan bisnis Anda ke tingkat ahli untuk mempelajari cara membaca *Link Phishing Palsu*, mengunci keamanan *WhatsApp Toko*, dan mengunduh *Sertifikat Kelulusan Resmi Toko*.")
    st.markdown("---")
    st.write("👉 **Hubungi kami via WhatsApp di bawah ini untuk membuka seluruh materi (Hanya Rp 50.000):**")
    st.button("Ajukan Kode Pembuka Akses via Email/WhatsApp")

# ----------------- MATERI 1 -----------------
elif menu == m1:
    st.markdown(f"### 📘 {m1}")
    st.write(
        "Di dunia siber, peretas jarang membobol sistem enkripsi bank yang berlapis baja. "
        "Mereka memilih meretas jalur paling rapuh: **Psikologi Manusia**. *Social Engineering* adalah "
        "teknik manipulasi di mana penipu memanfaatkan celah emosi Anda agar Anda melakukan kesalahan fatal "
        "(seperti memberikan PIN atau mengeklik link berbahaya) secara sukarela."
    )
    st.info("💡 **Trik Lapangan:** Jika menerima pesan yang memicu emosi ekstrem (sangat panik/sangat senang), logika Anda sedang diserang. Diamkan pesan itu selama 10 menit agar otak kembali tenang.")
    
    st.markdown("---")
    st.subheader("✍️ UJIAN MANDIRI MATERI 1")
    st.write("Mengapa pelaku penipuan digital lebih sering mengincar korban manusia secara langsung dibandingkan membobol sistem pertahanan server perbankan?")
    
    terkunci = "m1" in st.session_state.materi_selesai
    pilihan_1 = st.radio(
        "Pilih jawaban Anda:",
        [
            "A. Karena membobol akun perorangan bisa otomatis mendapatkan akses ke seluruh server pusat bank.",
            "B. Karena manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank.",
            "C. Karena sistem keamanan m-banking di Indonesia belum memiliki enkripsi pelindung sama sekali.",
            "D. Karena penipu tidak memiliki komputer yang cukup canggih untuk melakukan peretasan sistem."
        ],
        index=None,
        disabled=terkunci,
        key="q1"
    )
    
    if pilihan_1 and not terkunci:
        if st.button("Kunci Jawaban (Tidak Bisa Diubah)", key="btn1"):
            kunci_jawaban("m1", pilihan_1, "B")
            st.rerun()
            
    if terkunci:
        st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
        jawaban_tercatat = st.session_state.get("q1")
        if jawaban_tercatat and "B" in jawaban_tercatat:
            st.success("✅ **BENAR!** Anda paham fondasinya. Penipu tahu meretas emosi manusia jauh lebih murah dan cepat daripada meretas kode server bank.")
        else:
            st.error("❌ **SALAH!** Celah terbesar bukan pada kelemahan sistem komputer, melainkan pada manipulasi psikologis manusia itu sendiri.")

# ----------------- MATERI 2 -----------------
elif menu == m2:
    st.markdown(f"### 📘 {m2}")
    st.write(
        "Penipu mengirim SMS/WhatsApp menggunakan nomor biasa, menyatakan bahwa rekening Bank atau e-wallet (Dana/OVO) Anda terancam dibekukan karena aktivitas mencurigakan. "
        "Untuk membatalkan pemblokiran, Anda dipaksa mengeklik tautan yang disediakan dalam waktu singkat."
    )
    st.info("💡 **Trik Lapangan:** Bank resmi tidak pernah meminta nasabah melakukan konfirmasi pemblokiran atau pembaruan data tarif melalui tautan di SMS/WhatsApp nomor pribadi nasabah.")
    
    st.markdown("---")
    st.subheader("✍️ UJIAN MANDIRI MATERI 2")
    st.write("Anda menerima SMS dari nomor handphone biasa: 'AKUN BANK ANDA DIBLOKIR. Untuk mengaktifkan kembali, silakan verifikasi data Anda di bca-validasi-data.com dalam waktu 2 jam atau saldo Anda hangus.' Apa tindakan paling tepat?")
    
    terkunci = "m2" in st.session_state.materi_selesai
    pilihan_2 = st.radio(
        "Pilih jawaban Anda:",
        [
            "A. Segera klik tautan tersebut untuk memverifikasi data sebelum batas waktu 2 jam habis agar saldo aman.",
            "B. Membalas SMS tersebut dengan kata-kata kasar untuk menakut-nakuti penipu.",
            "C. Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.",
            "D. Mentransfer seluruh saldo ke rekening saudara agar tidak bisa disedot oleh sistem bank."
        ],
        index=None,
        disabled=terkunci,
        key="q2"
    )
    
    if pilihan_2 and not terkunci:
        if st.button("Kunci Jawaban (Tidak Bisa Diubah)", key="btn2"):
            kunci_jawaban("m2", pilihan_2, "C")
            st.rerun()
            
    if terkunci:
        st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
        jawaban_tercatat = st.session_state.get("q2")
        if jawaban_tercatat and "C" in jawaban_tercatat:
            st.success("✅ **BENAR!** Mengabaikan dan mengecek langsung ke jalur resmi adalah benteng pertahanan terbaik terhadap modus kepanikan (urgency).")
        else:
            st.error("❌ **SALAH & BAHAYA!** Mengeklik tautan tersebut akan mengantarkan Anda ke website palsu yang siap merekam data kartu ATM dan PIN Anda.")

# ----------------- MATERI 3 -----------------
elif menu == m3:
    st.markdown(f"### 📘 {m3}")
    st.write(
        "Penipu menyamar sebagai Customer Service (CS) bank atau perusahaan fintech di WhatsApp. Agar korban percaya, pelaku memasang foto profil "
        "berlogo perusahaan yang di bagian pojok bawahnya **diedit gambar lingkaran centang hijau kecil** seolah-olah akun tersebut telah terverifikasi resmi (*Verified Account*)."
    )
    st.info("💡 **Trik Lapangan:** Akun resmi WhatsApp yang memiliki centang hijau asli, lambang centangnya akan selalu berada di **sebelah kanan nama akun**, bukan tertanam di dalam lingkaran foto profilnya.")
    
    st.markdown("---")
    st.subheader("✍️ UJIAN MANDIRI MATERI 3")
    st.write("Bagaimana cara paling akurat untuk membedakan antara akun Customer Service bank resmi dengan akun CS penipu di platform WhatsApp?")
    
    terkunci = "m3" in st.session_state.materi_selesai
    pilihan_3 = st.radio(
        "Pilih jawaban Anda:",
        [
            "A. Melihat apakah ada lambang centang hijau di dalam foto profil akun WhatsApp tersebut.",
            "B. Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan.",
            "C. Mengecek apakah nomor WhatsApp tersebut menggunakan kode telepon luar negeri atau lokal.",
            "D. Mengukur tingkat keramahan bahasa chat yang digunakan oleh admin CS tersebut."
        ],
        index=None,
        disabled=terkunci,
        key="q3"
        )
    if pilihan_3 and not terkunci:
        if st.button("Kunci Jawaban (Tidak Bisa Diubah)", key="btn3"):
            kunci_jawaban("m3", pilihan_3, "B")
            st.rerun()
    if terkunci:
        st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
        jawaban_tercatat = st.session_state.get("q3")
        if jawaban_tercatat and "B" in jawaban_tercatat:
            st.success("✅ BENAR! Deteksi visual Anda sangat tajam. Centang hijau resmi tidak akan bisa dimanipulasi ke dalam baris nama akun oleh penipu, mereka hanya bisa mengedit foto profil.")
        else:
            st.error("❌ SALAH! Jika Anda terkecoh melihat centang hijau di dalam foto profil, Anda akan dengan mudah menyerahkan data rahasia kepada penipu.")

#----------------- MATERI 4 -----------------
elif menu == m4:
    st.markdown(f"### 📘 {m4}")
    st.write(
        "Pelaku menelepon korban secara langsung, menyamar menjadi Polisi, menyatakan anak/saudara Anda ditangkap karena kasus narkoba/tawuran, dan meminta uang damai instan. ""Jika korban mengaku tidak punya uang di tabungan, pelaku akan memandu korban lewat telepon untuk mengaktifkan fitur Paylater atau Pinjaman Online di aplikasi Shopee/Gojek, lalu mencairkannya ke rekening pelaku."
    )
    st.info("💡 Trik Lapangan: Institusi kepolisian resmi tidak pernah meminta uang damai lewat telepon, dan tidak ada polisi yang meminta warga mencairkan dana utang Paylater.")
    st.markdown("---")
    st.subheader("✍️ UJIAN MANDIRI MATERI 4")
    st.write("Seseorang menelepon Anda mengaku sebagai Polisi, menyatakan anak Anda ditangkap. Dia meminta Rp 5 Juta. Saat Anda billing tidak punya uang, dia membimbing Anda untuk membuka aplikasi belanja dan mengaktifkan limit Paylater untuk ditransfer ke dia. Tindakan Anda?")
        
    terkunci = "m4" in st.session_state.materi_selesai
    pilihan_4 = st.radio(
        "Pilih jawaban Anda:",
        [
            "A. Mengikuti arahannya untuk mengaktifkan Paylater demi menyelamatkan anak yang sedang ditahan polisi.",
            "B. Meminta keringanan harga uang damai agar tidak perlu mencairkan utang paylater terlalu besar.",
            "C. Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater.",
            "D. Datang ke kantor polisi terdekat sendirian tanpa mencoba menghubungi anak terlebih dahulu."
        ],
        index=None,
        disabled=terkunci,
        key="q4"
        )
    if pilihan_4 and not terkunci:
        if st.button("Kunci Jawaban (Tidak Bisa Diubah)", key="btn4"):
            kunci_jawaban("m4", pilihan_4, "C")
            st.rerun()
    if terkunci:
        st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
        jawaban_tercatat = st.session_state.get("q4")
        if jawaban_tercatat and "C" in jawaban_tercatat:
            st.success("✅ BENAR! Memutus kontak dan melakukan verifikasi mandiri adalah cara mutlak untuk menghancurkan skenario hipnotis telepon penipu.")
        else:
            st.error("❌ SALAH & TRAGIS! Mengikuti arahan pelaku akan membuat Anda menanggung utang paylater bulanan, padahal anak Anda sebenarnya aman-aman saja.")

#----------------- HALAMAN RAPOR (PIE CHART) -----------------
elif menu == m_rapor:
    st.markdown(f"### {m_rapor}")
    st.write("Halaman ini menganalisis insting pertahanan Anda berdasarkan materi kuis yang sudah diselesaikan.")
    total_jawab = len(st.session_state.materi_selesai)
    if total_jawab == 0:
        st.info("ℹ️ Rapor belum tersedia. Silakan kerjakan kuis pada Materi 1 sampai Materi 4 terlebih dahulu.")
    else:
            st.metric("Total Soal Selesai", f"{total_jawab} / 4 Soal")
            labels = ['Insting Aman (Benar)', 'Celah Bahaya (Salah)']
            sizes = [st.session_state.skor_aman, st.session_state.skor_bahaya]
            colors = ['#2ECC71', '#E74C3C']
            chart_data = []
            chart_labels = []
            chart_colors = []
            for l, s, c in zip(labels, sizes, colors):
                if s > 0:
                    chart_data.append(s)
                    chart_labels.append(f"{l} ({s} Soal)")
                    chart_colors.append(c)
                    fig, ax = plt.subplots(figsize=(6, 4))
                    ax.pie(chart_data, labels=chart_labels, colors=chart_colors, autopct='%1.1f%%', 
                    startangle=90, textprops={'color':"white"})
                    ax.axis('equal')
                    fig.patch.set_facecolor('#1E1E1E')
                    ax.set_facecolor('#1E1E1E')
                    st.pyplot(fig)
                    st.markdown("### 📝 Analisis Hasil Konsultan:")
                    if st.session_state.skor_aman == 4:
                        st.success("👑 LEVEL: GARDA UTAMA. Selamat! Insting digital Anda sangat sempurna. Anda sangat sulit ditembus oleh taktik manipulasi psikologis penipu online.")
elif st.session_state.skor_aman >= 2:
    st.warning("⚠️ LEVEL: WASPADA SEDANG. Pertahanan Anda lumayan, namun Anda masih memiliki celah emosional yang bisa dimanfaatkan penipu jika Anda sedang lengah atau panik.")
else:
    st.error("🚨 LEVEL: RAWAN TINGGI. Sangat Bahaya! Anda sangat mudah terpancing oleh modus kepanikan dan manipulasi penipu. Anda wajib mengulang materi agar rekening tabungan tidak ludes di dunia nyata.")
