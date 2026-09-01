import streamlit as st
import matplotlib.pyplot as plt

# 1. Pengaturan Awal Tampilan Halaman Web
st.set_page_config(page_title="GardaDigital", page_icon="🛡️", layout="centered")

# =========================================================================
# 🧠 SISTEM INTEGRASI DATABASE JAWABAN REAL-TIME (SESSION STATE)
# =========================================================================
if "jumlah_pengulangan" not in st.session_state:
    st.session_state.jumlah_pengulangan = 0
if "jawaban_user" not in st.session_state:
    st.session_state.jawaban_user = {}  # Menyimpan kunci jawaban: {"m1": "B", "m2": "C"}
if "materi_selesai" not in st.session_state:
    st.session_state.materi_selesai = set()

# Kunci data materi agar 100% akurat
KUNCI_MATERI = {"m1": "B", "m2": "C", "m3": "B", "m4": "C"}

# =========================================================================
# 🧭 STRUKTUR SIDEBAR BERTINGKAT (MODUL -> MATERI)
# =========================================================================
st.sidebar.title("🛡️ Panel Navigasi")

modul_terpilih = st.sidebar.selectbox(
    "Pilih Modul Pelatihan:",
    [
        "Modul 1: Social Engineering (Gratis)",
        "Modul 2: Digital Phishing & Link Palsu (🔒 Premium)",
        "Modul 3: Mengunci Brankas & Aset Bisnis (🔒 Premium)",
        "Modul 4: Sertifikasi & Manajemen Krisis (🔒 Premium)"
    ]
)

m0 = "[ Baca Beranda Utama & Moto ]"
m1 = "Materi 1: Pengenalan Social Engineering"
m2 = "Materi 2: Ancaman Pemblokiran Rekening"
m3 = "Materi 3: Fake CS (Centang Hijau Palsu)"
m4 = "Materi 4: Vishing (Telepon Polisi Palsu)"
m_rapor = "📊 Rapor Hasil Evaluasi Saya"

if "Modul 1" in modul_terpilih:
    menu = st.sidebar.selectbox("Pilih Pembelajaran:", [m0, m1, m2, m3, m4, m_rapor])
else:
    menu = "[ Terkunci 🔒 ]"
    st.sidebar.warning("🔒 Modul ini hanya bisa diakses oleh member Premium seharga Rp 50.000.")

# =========================================================================
# 🏛️ KONTEN HALAMAN TENGAH WEBSITE (TERISOLASI SEMPURNA)
# =========================================================================

# ----------------- HALAMAN BERANDA / LOGO UTAMA -----------------
if menu == m0:
    st.write("") 
    col1, col2, col3 = st.columns(3)
    with col2:
        st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; margin-top: 0px; font-size: 32px;'>GardaDigital</h1>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #BDC3C7; font-size: 18px;'>\"Membangun Perisai Siber Akal Sehat, Melindungi Aset Toko & Rekening Tabungan Anda.\"</h3>", unsafe_allow_html=True)
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

# ----------------- PROGRAM MATERI 1 SAMPAI 4 -----------------
elif menu in [m1, m2, m3, m4]:
    # Pemetaan variabel lokal kustom per materi
    if menu == m1:
        mid, judul, soal, kunci = "m1", m1, "Menganya pelaku penipuan digital lebih sering mengincar korban manusia secara langsung dibandingkan membobol sistem pertahanan server perbankan?", "B"
        opsi = [
            "A. Karena membobol akun perorangan bisa otomatis mendapatkan akses ke seluruh server pusat bank.",
            "B. Karena manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank [💡].",
            "C. Karena sistem keamanan m-banking di Indonesia belum memiliki enkripsi pelindung sama sekali.",
            "D. Karena penipu tidak memiliki komputer yang cukup canggih untuk melakukan peretasan sistem."
        ]
        isi_teks = "Di dunia siber, peretas jarang membobol sistem enkripsi bank yang berlapis baja. Mereka memilih meretas jalur paling rapuh: **Psikologi Manusia**. *Social Engineering* adalah teknik manipulasi di mana penipu memanfaatkan celah emosi Anda agar Anda melakukan kesalahan fatal (seperti memberikan PIN atau mengeklik link berbahaya) secara sukarela [💡]."
        tips_teks = "Jika menerima pesan yang memicu emosi ekstrem (sangat panik/sangat senang), logika Anda sedang diserang. Diamkan pesan itu selama 10 menit agar otak kembali tenang."
    
    elif menu == m2:
        mid, judul, soal, kunci = "m2", m2, "Anda menerima SMS dari nomor handphone biasa: 'AKUN BANK ANDA DIBLOKIR. Untuk mengaktifkan kembali, silakan verifikasi data Anda di bca-validasi-data.com.' Apa tindakan paling tepat?", "C"
        opsi = [
            "A. Segera klik tautan tersebut untuk memverifikasi data sebelum batas waktu habis agar saldo aman.",
            "B. Membalas SMS tersebut dengan kata-kata kasar untuk menakut-nakuti penipu.",
            "C. Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat [💡].",
            "D. Mentransfer seluruh saldo ke rekening saudara agar tidak bisa disedot oleh sistem bank."
        ]
        isi_teks = "Penipu mengirim SMS/WhatsApp menggunakan nomor biasa, menyatakan bahwa rekening Bank atau e-wallet (Dana/OVO) Anda terancam dibekukan karena aktivitas mencurigakan [💡]. Untuk membatalkan pemblokiran, Anda dipaksa mengeklik tautan yang disediakan dalam waktu singkat."
        tips_teks = "Bank resmi tidak pernah meminta nasabah melakukan konfirmasi pemblokiran atau pembaruan data tarif melalui tautan di SMS/WhatsApp nomor pribadi nasabah [💡]."

    elif menu == m3:
        mid, judul, soal, kunci = "m3", m3, "Bagaimana cara paling akurat untuk membedakan antara akun Customer Service bank resmi dengan akun CS penipu di platform WhatsApp?", "B"
        opsi = [
            "A. Melihat apakah ada lambang centang hijau di dalam foto profil akun WhatsApp tersebut.",
            "B. Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan [💡].",
            "C. Mengecek apakah nomor WhatsApp tersebut menggunakan kode telepon luar negeri atau lokal.",
            "D. Mengukur tingkat keramahan bahasa chat yang digunakan oleh admin CS tersebut."
        ]
        isi_teks = "Penipu menyamar sebagai Customer Service (CS) bank atau perusahaan fintech di WhatsApp [💡]. Agar korban percaya, pelaku memasang foto profil berlogo perusahaan yang di bagian pojok bawahnya **diedit gambar lingkaran centang hijau kecil** seolah-olah akun tersebut telah terverifikasi resmi (*Verified Account*)."
        tips_teks = "Akun resmi WhatsApp yang memiliki centang hijau asli, lambang centangnya akan selalu berada di **sebelah kanan nama akun**, bukan tertanam di dalam lingkaran foto profilnya."

    elif menu == m4:
        mid, judul, soal, kunci = "m4", m4, "Seseorang menelepon Anda mengaku sebagai Polisi, menyatakan anak Anda ditangkap. Dia meminta Rp 5 Juta. Saat Anda bilang tidak punya uang, dia membimbing Anda untuk membuka aplikasi belanja dan mengaktifkan limit Paylater untuk ditransfer ke dia. Tindakan Anda?", "C"
        opsi = [
            "A. Mengikuti arahannya untuk mengaktifkan Paylater demi menyelamatkan anak yang sedang ditahan polisi.",
            "B. Meminta keringanan harga uang damai agar tidak perlu mencairkan utang paylater terlalu besar.",
            "C. Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater [💡].",
            "D. Datang ke kantor polisi terdekat sendirian tanpa mencoba menghubungi anak terlebih dahulu."
        ]
        isi_teks = "Pelaku menelepon korban secara langsung, menyamar menjadi Polisi, menyatakan anak/saudara Anda ditangkap karena kasus narkoba/tawuran, dan meminta uang damai instan [💡]. Jika korban mengaku tidak punya uang di tabungan, pelaku akan memandu korban lewat telepon untuk mengaktifkan fitur **Paylater** atau **Pinjaman Online** di aplikasi Shopee/Gojek, lalu mencairkannya ke rekening pelaku [💡]."
        tips_teks = "Institusi kepolisian resmi tidak pernah meminta uang damai lewat telepon, dan tidak ada polisi yang meminta warga mencairkan dana utang Paylater."

    st.markdown(f"### 📘 {judul}")
    st.write(isi_teks)
    st.info(f"💡 **Trik Lapangan:** {tips_teks}")
    st.markdown("---")
    st.subheader("✍️ UJIAN MANDIRI")
    st.write(soal)
    
    terkunci = mid in st.session_state.materi_selesai
    
    # Membaca jawaban ter-save agar tombol radio tidak reset sendiri
    index_default = None
    if terkunci:
        jawaban_lama = st.session_state.jawaban_user.get(mid, "")
        for idx, o in enumerate(opsi):
            if o.startswith(jawaban_lama):
                index_default = idx

    pilihan = st.radio("Pilih jawaban Anda:", opsi, index=index_default, disabled=terkunci, key=f"radio_{mid}")
    
    if pilihan and not terkunci:
        if st.button("Kunci Jawaban (Tidak Bisa Diubah)", key=f"btn_{mid}"):
            st.session_state.materi_selesai.add(mid)
            st.session_state.jawaban_user[mid] = pilihan[0] # Menyimpan huruf depan aja (A/B/C/D)
            st.rerun()
            
    if terkunci:
        st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
        if st.session_state.jawaban_user.get(mid) == kunci:
            st.success("✅ **BENAR!** Jawaban Anda sangat tepat. Insting keamanan digital Anda berfungsi sempurna.")
        else:
            st.error("❌ **SALAH!** Anda terjebak rekayasa sosial pelaku. Baca kembali trik lapangan di atas!")

# ----------------- HALAMAN RAPOR (KUNCI DI DALAM RUMPUN SINKRON) -----------------
elif menu == m_rapor:
    st.markdown(f"### {m_rapor}")
    
    total_jawab = len(st.session_state.materi_selesai)
    if total_jawab < 4:
        st.info(f"ℹ️ Rapor belum lengkap. Anda baru menyelesaikan {total_jawab} dari 4 soal. Silakan selesaikan seluruh kuis materi terlebih dahulu.")
    else:
        # Menhitung skor akhir secara dinamis dari database tanpa bocor
        skor_aman = 0
        skor_bahaya = 0
        for m_id, k in KUNCI_MATERI.items():
            if st.session_state.jawaban_user.get(m_id) == k:
                skor_aman += 1
            else:
                skor_bahaya += 1
                
        st.metric("Jumlah Upaya Percobaan Pelatihan", f"Percobaan Ke-{st.session_state.jumlah_pengulangan + 1}")
        
        # 📈 PENYELARASAN 2 PIE CHART (DIREKREASI SEJAJAR SAMA BESAR)
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🎯 Akurasi Materi Saat Ini</p>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(3, 3)) # Memastikan ukuran box 3x3 inci
            ax1.pie([skor_aman, skor_bahaya], labels=[f"Aman ({skor_aman})", f"Celah ({skor_bahaya})"], colors=['#2ECC71', '#E74C3C'], autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax1.axis('equal')  
            fig1.patch.set_facecolor('#1E1E1E')
            ax1.set_facecolor('#1E1E1E')
            st.pyplot(fig1)
            
        with col_chart2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🔄 Status Kelulusan Sistem</p>", unsafe_allow_html=True)
            sizes2 = [100, 0] if skor_aman == 4 else [0, 100]
            labels2 = ['Lulus 100%', 'Wajib Remidi'] if skor_aman == 4 else ['Lulus 100%', 'Wajib Remidi']
            colors2 = ['#2ECC71', '#555555'] if skor_aman == 4 else ['#555555', '#E74C3C']
            
            fig2, ax2 = plt.subplots(figsize=(3, 3)) # Di-lock ukuran box-nya agar sama besar dan seimbang
            ax2.pie(sizes2, labels=labels2, colors=colors2, autopct='%1.0f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax2.axis('equal')  
            fig2.patch.set_facecolor('#1E1E1E')
            ax2.set_facecolor('#1E1E1E')
            st.pyplot(fig2)

        st.markdown("---")
        st.markdown("### 📝 Analisis Hasil Konsultan:")
        
        if skor_aman == 4:
            st.success("👑 **LEVEL: GARDA UTAMA (LULUS 100%)**\n\nSelamat! Insting digital Anda sangat sempurna tanpa cacat. Anda resmi dinyatakan lulus sertifikasi mandiri GardaDigital. Sistem mengunci status Anda sebagai akun aman!")
        else:
            st.error(f"🚨 **LEVEL: BELUM LULUS (TERDETEKSI CELAH BAHAYA)**\n\nAnda menjawab benar {skor_aman} soal dan salah {skor_bahaya} soal. Sistem mendeteksi psikologi Anda masih rawan dijebak penipu di dunia nyata!")
            st.warning("⚠️ **ATURAN PRIVASI KORPORASI:** Anda tidak diizinkan membuka modul premium lanjutan sebelum Anda berhasil menyelesaikan seluruh kuis dengan skor **100% BENAR (4/4)**.")
            
            if st.button("🔄 Ulangi Pelatihan Sekarang (Reset & Hitung Pengulangan)", type="primary"):
                st.session_state.jumlah_pengulangan += 1
                st.session_state.jawaban_user = {}
                st.session_state.materi_selesai = set()
                st.rerun()