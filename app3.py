import streamlit as st
import matplotlib.pyplot as plt

# 1. Pengaturan Awal Tampilan Halaman Web
st.set_page_config(page_title="GardaDigital", page_icon="🛡️", layout="centered")

# =========================================================================
# 🧠 DATABASE INTERNAL: STATUS HALAMAN & SKOR JAWABAN (SESSION STATE)
# =========================================================================
if "halaman_sekarang" not in st.session_state:
    st.session_state.halaman_sekarang = 0  # 0 = Beranda, 1-4 = Materi, 5 = Rapor

if "jumlah_pengulangan" not in st.session_state:
    st.session_state.jumlah_pengulangan = 0

if "jawaban_user" not in st.session_state:
    st.session_state.jawaban_user = {}

if "materi_selesai" not in st.session_state:
    st.session_state.materi_selesai = set()

# Database Kunci Jawaban Mutlak (Mencocokkan kalimat persis agar bebas bug)
KUNCI_MATERI = {
    "m1": "Manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi",
    "m2": "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi",
    "m3": "Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun",
    "m4": "Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri"
}

# =========================================================================
# 🧭 SIDEBAR MINIMALIS: HANYA PILIHAN MODUL
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

if st.sidebar.button("🏠 Kembali ke Beranda Utama"):
    st.session_state.halaman_sekarang = 0
    st.rerun()

# =========================================================================
# 🏛️ FILTER KUNCI GERBANG JIKA USER MEMILIH MODUL PREMIUM
# =========================================================================
if "Modul 1" not in modul_terpilih:
    st.markdown(f"### 🔒 Akses Terkunci: {modul_terpilih}")
    st.error("Maaf, modul ini masuk ke dalam paket materi lanjutan (Premium member).")
    st.write("Tingkatkan pertahanan bisnis Anda ke tingkat ahli untuk mempelajari cara membaca *Link Phishing Palsu*, mengunci keamanan *WhatsApp Toko*, dan mengunduh *Sertifikat Kelulusan Resmi Toko*.")
    st.markdown("---")
    st.write("👉 **Hubungi kami via WhatsApp di bawah ini untuk membuka seluruh materi (Hanya Rp 50.000):**")
    st.button("Ajukan Kode Pembuka Akses via Email/WhatsApp")

# =========================================================================
# 🏛️ EKSEKUSI JALUR HALAMAN LINEAR (LEVEL SYSTEM) MODUL 1
# =========================================================================
else:
    # ----------------- HALAMAN 0: BERANDA UTAMA -----------------
    if st.session_state.halaman_sekarang == 0:
        st.write("") 
        col1, col2, col3 = st.columns(3)
        with col2:
            st.markdown("<h1 style='text-align: center; font-size: 80px; margin-bottom: 0px;'>🛡️</h1>", unsafe_allow_html=True)
            st.markdown("<h1 style='text-align: center; margin-top: 0px; font-size: 32px;'>GardaDigital</h1>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='text-align: center; color: #BDC3C7; font-size: 18px;'>\"Membangun Perisai Siber Akal Sehat, Melindungi Aset Toko & Rekening Tabungan Anda.\"</h3>", unsafe_allow_html=True)
        st.markdown("---")
        st.write("👋 **Selamat Datang di Platform Sertifikasi Keamanan Digital Mandiri GardaDigital.**")
        st.write("Sistem ini dirancang menggunakan sistem linear bertingkat. Anda akan membaca cerita studi kasus berdasarkan realitas di Indonesia, melihat contoh visual simulasi serangan peretas, dan wajib menyelesaikan tes di setiap akhir materi.")
        
        st.write("")
        if st.button("🚀 Memulai Pelatihan Modul 1 (Materi 1)", type="primary", use_container_width=True):
            st.session_state.halaman_sekarang = 1
            st.rerun()

    # ----------------- HALAMAN 1: MATERI 1 (STORI PANJANG AUDIT TOKO) -----------------
    elif st.session_state.halaman_sekarang == 1:
        st.markdown("### 📘 MATERI 1: Pengenalan Social Engineering (Sistem vs Manusia)")
        st.markdown("""
        **Skenario Studi Kasus: Jebakan Toko Hijab Online**
        
        Siti adalah seorang ibu rumah tangga yang sukses mendirikan toko hijab online di marketplace. Suatu sore, saat pesanan sedang ramai, Siti menerima pesan WhatsApp dari nomor tidak dikenal yang menggunakan foto profil berlogo resmi e-commerce tempatnya berjualan.
        
        Pesan itu tertulis sangat formal: *'PEMBERITAHUAN AUDIT AKUN PENTING. Toko Anda terdeteksi melakukan pelanggaran manipulasi penjualan. Akun toko Anda akan DIBEKUKAN PERMANEN dalam waktu 10 menit, dan seluruh sisa saldo penjualan Anda akan ditarik oleh pusat, kecuali Anda segera melakukan verifikasi pembatalan audit.'*
        
        Siti mendadak lemas, jantungnya berdebar kencang, dan tangannya gemetar membayangkan jerih payahnya hilang. Di saat panik itulah, pelaku mengirimkan sebuah link dan meminta Siti memasukkan nomor HP serta kode rahasia yang masuk via SMS. Karena ketakutan, Siti menuruti semua kata pelaku. Dalam waktu 3 menit, akun toko Siti berhasil diambil alih oleh peretas dan uang penjualannya dikuras habis.
        
        Peretas tidak perlu meretas sistem pertahanan server marketplace yang dijaga ketat oleh tim IT ahli. Peretas cukup **meretas emosi dan kepanikan pikiran Siti (Manusia)**. Inilah yang disebut dengan teknik *Social Engineering* (Rekayasa Sosial).
        """)
        
        st.info("💡 **Trik Lapangan:** Jika menerima pesan yang memicu emosi ekstrem (sangat panik atau sangat senang), logika Anda sedang dilumpuhkan. Diamkan pesan itu selama 10 menit agar otak kembali tenang sebelum mengambil tindakan.")
        st.markdown("---")
        
        st.subheader("✍️ UJIAN MANDIRI MATERI 1")
        st.write("Mengapa pelaku penipuan digital lebih sering mengincar korban manusia secara langsung dibandingkan membobol sistem pertahanan server perbankan/marketplace?")
        
        terkunci = "m1" in st.session_state.materi_selesai
        
        opsi_1 = [
            "Karena membobol akun perorangan bisa otomatis mendapatkan akses ke seluruh server pusat bank.",
            "Manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank.",
            "Karena sistem keamanan m-banking di Indonesia belum memiliki enkripsi pelindung sama sekali.",
            "Karena penipu tidak memiliki komputer yang cukup canggih untuk melakukan peretasan sistem."
        ]
        
        index_default = None
        if terkunci:
            jawaban_lama = st.session_state.jawaban_user.get("m1", "")
            if jawaban_lama in opsi_1:
                index_default = opsi_1.index(jawaban_lama)

        pilihan = st.radio("Pilih jawaban Anda:", opsi_1, index=index_default, disabled=terkunci, key="radio_m1")
        
        if pilihan and not terkunci:
            if st.button("Kunci Jawaban", key="btn_m1"):
                st.session_state.materi_selesai.add("m1")
                st.session_state.jawaban_user["m1"] = pilihan
                st.rerun()
                
        if terkunci:
            st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
            if KUNCI_MATERI["m1"] in st.session_state.jawaban_user.get("m1", ""):
                st.success("✅ **BENAR!** Anda paham fondasinya. Penipu tahu meretas emosi manusia jauh lebih murah dan cepat daripada meretas kode server bank.")
            else:
                st.error("❌ **SALAH!** Celah terbesar bukan pada kelemahan sistem komputer, melainkan pada manipulasi psikologis manusia itu sendiri.")
            
            if st.button("Materi Selanjutnya (Materi 2) ➡️", use_container_width=True):
                st.session_state.halaman_sekarang = 2
                st.rerun()

    # ----------------- HALAMAN 2: MATERI 2 (STORI PANJANG SMS BLANK REKENING) -----------------
    elif st.session_state.halaman_sekarang == 2:
        st.markdown("### 📘 MATERI 2: Ancaman Pemblokiran Rekening & E-Wallet (Modus Urgency)")
        st.markdown("""
        **Skenario Studi Kasus: SMS Tengah Malam Sang Pemilik Katering**
        
        Pak Budi adalah pengusaha katering kecil yang menaruh seluruh modal usahanya di rekening tabungan bank. Suatu malam jam 23.30 WIB, saat Pak Budi bersiap untuk tidur, sebuah SMS masuk dari nomor handphone biasa (bukan nomor resmi Alpha-Name Bank).
        
        Isi SMS itu berbunyi: *'Pemberitahuan Bank: Sistem mendeteksi transaksi tidak dikenal pada akun Anda. Akun Anda telah DIBLOKIR SEMENTARA demi keamanan. Untuk memulihkan akses dan menyelamatkan saldo Anda, silakan lakukan konfirmasi pembatalan pemblokiran di website resmi: bca-pembatalan-tarif-dana.com dalam waktu 2 jam.'*
        
        Membaca kata 'saldo Anda hangus', Pak Budi mendadak panik luar biasa. Logikanya mati karena takut modal belanja bahan katering besok pagi hilang. Tanpa memeriksa nomor pengirim, Pak Budi langsung mengeklik link tersebut. Dia diantarkan ke halaman website tiruan yang tampilannya 100% mirip dengan menu login mobile banking aslinya. Begitu Pak Budi mengetikkan nomor kartu ATM dan PIN, peretas langsung menguras habis seluruh isi tabungannya dalam hitungan detik.
        """)
        
        st.info("💡 **Trik Lapangan:** Bank resmi tidak pernah menggunakan nomor handphone biasa (+62...) untuk mengirimkan notifikasi penting, dan bank tidak pernah meminta konfirmasi pembatalan tarif atau data kartu nasabah melalui tautan di SMS.")
        st.markdown("---")
        
        st.subheader("✍️ UJIAN MANDIRI MATERI 2")
        st.write("Anda menerima SMS dari nomor handphone biasa: 'AKUN BANK ANDA DIBLOKIR. Untuk mengaktifkan kembali, silakan verifikasi data Anda di bca-validasi-data.com.' Apa tindakan paling tepat?")
        
        terkunci = "m2" in st.session_state.materi_selesai
        opsi_2 = [
            "Segera klik tautan tersebut untuk memverifikasi data sebelum batas waktu habis agar saldo aman.",
            "Membalas SMS tersebut dengan kata-kata kasar untuk menakut-nakuti penipu.",
            "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.",
            "Mentransfer seluruh saldo ke rekening saudara agar tidak bisa disedot oleh sistem bank."
        ]
        
        index_default = None
        if terkunci:
            jawaban_lama = st.session_state.jawaban_user.get("m2", "")
            if jawaban_lama in opsi_2:
                index_default = opsi_2.index(jawaban_lama)
                
        pilihan = st.radio("Pilih jawaban Anda:", opsi_2, index=index_default, disabled=terkunci, key="radio_m2")
        
        if pilihan and not terkunci:
            if st.button("Kunci Jawaban", key="btn_m2"):
                st.session_state.materi_selesai.add("m2")
                st.session_state.jawaban_user["m2"] = pilihan
                st.rerun()
                
        if terkunci:
            st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
            if KUNCI_MATERI["m2"] in st.session_state.jawaban_user.get("m2", ""):
                st.success("✅ **BENAR!** Mengabaikan dan mengecek langsung ke jalur resmi adalah benteng pertahanan terbaik terhadap modus kepanikan (urgency).")
            else:
                st.error("❌ **SALAH & BAHAYA!** Mengeklik tautan tersebut akan mengantarkan Anda ke website palsu yang siap merekam data kartu ATM dan PIN Anda.")
            
            if st.button("Materi Selanjutnya (Materi 3) ➡️", use_container_width=True):
                st.session_state.halaman_sekarang = 3
                st.rerun()

    # ----------------- HALAMAN 3: MATERI 3 (STORI CENTANG HIJAU PALSU) -----------------
    elif st.session_state.halaman_sekarang == 3:
        st.markdown("### 📘 MATERI 3: Fake CS - Akun WhatsApp Tiruan Berlogo Centang Hijau Palsu")
        st.markdown("""
        **Skenario Studi Kasus: Layanan Pengaduan Gadungan**
        
        Melanjutkan kisah Pak Budi yang panik, dia mencoba mencari nomor Customer Service bantuan di internet untuk menanyakan masalah SMS pemblokiran tadi. Sesaat kemudian, dia menemukan sebuah nomor WhatsApp yang memasang foto profil berlogo resmi Bank terkemuka.
        
        Saat Pak Budi melakukan chat, admin tersebut membalas dengan kalimat otomatis yang sangat sopan dan profesional. Di layar handphone Pak Budi, akun WhatsApp tersebut menampilkan simbol bulatan hijau kecil dengan centang putih di dalamnya. Pak Budi merasa sangat tenang karena mengira sedang berbicara dengan pihak berwenang resmi yang telah terverifikasi (Verified Business Account).
        
        Namun, Pak Budi lengah. Simbol centang hijau itu ternyata hanya gambar editan palsu yang ditempelkan oleh penipu ke dalam bulatan foto profilnya, bukan sistem centang hijau resmi dari pihak WhatsApp. Akibatnya, saat CS palsu itu meminta kode OTP 6 angka dengan alasan untuk membuka blokir tabungan, Pak Budi menyerahkannya begitu saja.
        """)
        
        st.info("💡 **Trik Lapangan:** Akun bisnis resmi WhatsApp yang memiliki lencana centang hijau asli, lambang centangnya akan selalu berada di sebelah kanan teks nama akun, bukan tertanam atau menempel di dalam gambar foto profil bulatannya.")
        st.markdown("---")
        
        st.subheader("✍️ UJIAN MANDIRI MATERI 3")
        st.write("Bagaimana cara paling akurat untuk membedakan antara akun Customer Service bank resmi dengan akun CS penipu di platform WhatsApp?")
        
        terkunci = "m3" in st.session_state.materi_selesai
        opsi_3 = [
            "Melihat apakah ada lambang centang hijau di dalam foto profil akun WhatsApp tersebut.",
            "Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan.",
            "Mengecek apakah nomor WhatsApp tersebut menggunakan kode telepon luar negeri atau lokal.",
            "Mengukur tingkat keramahan bahasa chat yang digunakan oleh admin CS tersebut."
        ]
        
        index_default = None
        if terkunci:
            jawaban_lama = st.session_state.jawaban_user.get("m3", "")
            if jawaban_lama in opsi_3:
                index_default = opsi_3.index(jawaban_lama)
                
        pilihan = st.radio("Pilih jawaban Anda:", opsi_3, index=index_default, disabled=terkunci, key="radio_m3")
        
        if pilihan and not terkunci:
            if st.button("Kunci Jawaban", key="btn_m3"):
                st.session_state.materi_selesai.add("m3")
                st.session_state.jawaban_user["m3"] = pilihan
                st.rerun()
                
        if terkunci:
            st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
            if KUNCI_MATERI["m3"] in st.session_state.jawaban_user.get("m3", ""):
                st.success("✅ **BENAR!** Deteksi visual Anda sangat tajam. Centang hijau resmi tidak akan bisa dimanipulasi ke dalam baris nama akun oleh penipu, mereka hanya bisa mengedit foto profil.")
            else:
                st.error("❌ **SALAH!** Jika Anda terkecoh melihat centang hijau di dalam foto profil, Anda akan dengan mudah menyerahkan data rahasia kepada penipu.")
            
            if st.button("Materi Selanjutnya (Materi 4) ➡️", use_container_width=True):
                st.session_state.halaman_sekarang = 4
                st.rerun()

    # ----------------- HALAMAN 4: MATERI 4 (STORI POLISI PALSU & PAYLATER) -----------------
    elif st.session_state.halaman_sekarang == 4:
        st.markdown("### 📘 MATERI 4: STORI POLISI PALSU & PAYLATER")
        st.markdown("""
        **Kronologi Studi Kasus Nyata di Indonesia:**
        
        Korban menerima panggilan telepon langsung dari nomor tidak dikenal. Suara di seberang mengaku sebagai Petugas Kepolisian berpangkat AKP dengan nada suara yang sangat tegas, membentak, dan berwibawa. Pelaku menyatakan bahwa anak/saudara kandung korban saat ini ditangkap di kantor polisi karena terlibat kasus tawuran massal atau narkoba.
        
        Pelaku menekan emosi korban agar panik dengan ancaman pidana 5 tahun penjara, namun menawarkan 'jalan damai kekeluargaan' jika korban mentransfer uang tebusan operasi/damai sebesar Rp 5 Juta dalam waktu 15 menit.
        
        Ketika korban menangis ketakutan dan mengaku tabungan ATM-nya kosong, pelaku tidak menutup telepon. Pelaku secara semi-hipnotis memandu korban:
        'Kamu punya aplikasi Shopee atau Gojek kan? Buka sekarang! Cari tulisan Paylater atau Pinjaman Instan, klik aktifkan sekarang juga! Jangan dimatikan teleponnya, saya pandu agar limit utangnya cair sekarang untuk menyelamatkan keluarga kamu!'
        
        Korban yang berada dalam kondisi panik luar biasa menuruti instruksi tersebut, mencairkan dana talangan utang Paylater, dan mengirimkannya ke rekening peretas. Di akhir cerita, korban baru menyadari bahwa anggota keluarganya ternyata aman-aman saja berada di sekolah. Uang lenyap, utang cicilan menumpuk.
        """)
        
        st.info("💡 **Trik Lapangan:** Institusi kepolisian resmi tidak pernah meminta uang damai lewat telepon, dan tidak ada polisi di dunia ini yang berwenang menyuruh warga mencairkan dana utang Paylater.")
        st.markdown("---")
        st.subheader("✍️ UJIAN MANDIRI MATERI 4")
        st.write("Seseorang menelepon Anda mengaku sebagai Polisi, menyatakan anak Anda ditangkap. Dia meminta Rp 5 Juta. Saat Anda bilang tidak punya uang, dia membimbing Anda untuk membuka aplikasi belanja dan mengaktifkan limit Paylater untuk ditransfer ke dia. Tindakan Anda?")
        
        terkunci = "m4" in st.session_state.materi_selesai
        opsi_4 = [
            "Mengikuti arahannya untuk mengaktifkan Paylater demi menyelamatkan anak yang sedang ditahan polisi.",
            "Meminta keringanan harga uang damai agar tidak perlu mencairkan utang paylater terlalu besar.",
            "Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater.",
            "Datang ke kantor polisi terdekat sendirian tanpa mencoba menghubungi anak terlebih dahulu."
        ]
        
        index_default = None
        if terkunci:
            jawaban_lama = st.session_state.jawaban_user.get("m4", "")
            if jawaban_lama in opsi_4:
                index_default = opsi_4.index(jawaban_lama)
                
        pilihan = st.radio("Pilih jawaban Anda:", opsi_4, index=index_default, disabled=terkunci, key="radio_m4")
        
        if pilihan and not terkunci:
            if st.button("Kunci Jawaban", key="btn_m4"):
                st.session_state.materi_selesai.add("m4")
                st.session_state.jawaban_user["m4"] = pilihan
                st.rerun()
                
        if terkunci:
            st.warning("🔒 Jawaban Anda sudah dikunci dan tidak bisa diubah kembali.")
            if KUNCI_MATERI["m4"] in st.session_state.jawaban_user.get("m4", ""):
                st.success("✅ **BENAR!** Memutus kontak dan melakukan verifikasi mandiri adalah cara mutlak untuk menghancurkan skenario hipnotis telepon penipu.")
            else:
                st.error("❌ **SALAH & TRAGIS!** Mengikuti arahan pelaku akan membuat Anda menanggung utang paylater bulanan, padahal anak Anda sebenarnya aman-aman saja.")
            
            if st.button("Buka Halaman Rapor Hasil Evaluasi Akhir 📊", use_container_width=True, type="primary"):
                st.session_state.halaman_sekarang = 5
                st.rerun()

    # ----------------- HALAMAN 5: RAPOR EVALUASI AKHIR (PIE CHART) -----------------
    elif st.session_state.halaman_sekarang == 5:
        st.markdown("RAPOR EVALUASI AKHIR")
        
        skor_aman = 0
        skor_bahaya = 0
        for m_id, k in KUNCI_MATERI.items():
            if st.session_state.jawaban_user.get(m_id) and k in st.session_state.jawaban_user.get(m_id):
                skor_aman += 1
            else:
                skor_bahaya += 1
                
        st.metric("Jumlah Upaya Percobaan Pelatihan", f"Percobaan Ke-{st.session_state.jumlah_pengulangan + 1}")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🎯 Akurasi Materi Saat Ini</p>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(3, 3))
            ax1.pie([skor_aman, skor_bahaya], labels=[f"Aman ({skor_aman})", f"Celah ({skor_bahaya})"], colors=['#2ECC71', '#E74C3C'], autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax1.axis('equal')  
            fig1.patch.set_facecolor('#1E1E1E')
            ax1.set_facecolor('#1E1E1E')
            st.pyplot(fig1)
            
        with col_chart2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🔄 Status Kelulusan Sistem</p>", unsafe_allow_html=True)
            sizes2 = [100, 0] if skor_aman == 4 else [0, 100]
            labels2 = ['Lulus 100%', ''] if skor_aman == 4 else ['', 'Wajib Remidi']
            colors2 = ['#2ECC71', '#555555'] if skor_aman == 4 else ['#555555', '#E74C3C']
            
            fig2, ax2 = plt.subplots(figsize=(3, 3))
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
            
            if st.button("🔄 Ulangi Pelatihan Sekarang (Reset & Hitung Pengulangan)", type="primary", use_container_width=True):
                st.session_state.jumlah_pengulangan += 1
                st.session_state.jawaban_user = {}
                st.session_state.materi_selesai = set()
                st.session_state.halaman_sekarang = 1
                st.rerun()
