import streamlit as st
import sqlite3
import random
import matplotlib.pyplot as plt
import os

# 1. Pengaturan Awal Tampilan Halaman Web
st.set_page_config(page_title="GardaDigital - Sistem Akun & Anti-Cheat", page_icon="🛡️", layout="centered")

# =========================================================================
# 💾 ENGINE DATABASE LOKAL (SQLITE3) - URUTAN FIX ANTI-NAMEERROR
# =========================================================================
def hubungkan_db():
    # Fungsi ini wajib ditulis paling pertama agar bisa dibaca oleh fungsi di bawahnya
    conn = sqlite3.connect("gardadigital.db")
    return conn

def buat_tabel_database():
    conn = hubungkan_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengguna (
            email TEXT PRIMARY KEY,
            password TEXT,
            remidi_b1 INTEGER DEFAULT 0,
            remidi_b2 INTEGER DEFAULT 0,
            halaman_terakhir INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    
    # Suntikan otomatis pengaman kolom jika database lama Anda menolak di-reset
    try:
        cursor.execute("ALTER TABLE pengguna ADD COLUMN halaman_terakhir INTEGER DEFAULT 0")
        conn.commit()
    except sqlite3.OperationalError:
        pass
    conn.close()

# Panggil fungsi pembuatan tabel setelah kedua fungsi di atas selesai dideklarasikan
buat_tabel_database()


# =========================================================================
# 🧠 DATABASE KUNCI JAWABAN MUTLAK (UNTUK VALIDASI SKOR)
# =========================================================================
KUNCI_MATERI = {
    "m1": "Manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank.",
    "m2": "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.",
    "m3": "Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan.",
    "m4": "Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater.",
    "m5": "Menolak menginstal file tersebut, langsung menghapus pesan, and memeriksa status tilang secara mandiri melalui situs resmi ETLE Korlantas Polri menggunakan nomor pelat kendaraan.",
    "m6": "Menghapus pesan tersebut dan mengabaikannya, karena instansi pajak resmi tidak pernah mengirimkan dokumen penagihan denda atau detail pajak dalam format aplikasi APK lewat WhatsApp pribadi.",
    "m7": "Mengabaikan pesan WhatsApp tersebut dan memblokir nomornya, karena surat panggilan sidang resmi selalu dikirim melalui surat fisik pos tercatat ke alamat rumah.",
    "m8": "Keluar dari chat WhatsApp tersebut, lalu membuka aplikasi atau website resmi Seller Center marketplace secara mandiri untuk mengecek status toko yang sebenarnya.",
    "m9": "Mengabaikan pesan hoaks tersebut, tidak ikut menyebarkannya, and mengecek kebenaran informasi melalui situs resmi Bank Indonesia atau portal berita nasional yang terpercaya.",



}

# =========================================================================
# 🧠 INISIALISASI VARIABEL MEMORI (ANTI-BUG ATTRIBUTERROR)
# =========================================================================
if "login_sukses" not in st.session_state:
    st.session_state.login_sukses = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "halaman_sekarang" not in st.session_state:
    st.session_state.halaman_sekarang = 0  # 0=Beranda, 1=Intro, 2-5=M1-M4, 6=Rapor B1, 7=M5, 8=M6, 9=Rapor B2
if "jumlah_pengulangan_b1" not in st.session_state:
    st.session_state.jumlah_pengulangan_b1 = 0
if "jawaban_user" not in st.session_state:
    st.session_state.jawaban_user = {}
if "materi_selesai" not in st.session_state:
    st.session_state.materi_selesai = set()
# 👉 KUNCI PERBAIKAN: Mendeklarasikan objek dictionary kosong agar bebas dari AttributeError saat disubmit
if "pilihan_text_save" not in st.session_state:
    st.session_state.pilihan_text_save = {}


# =========================================================================
# 🎲 ENGINE PENGACAK JAWABAN BATCH 1 & 2
# =========================================================================
if "list_opsi_m1" not in st.session_state:
    opsi_m1 = ["Karena membobol akun perorangan bisa otomatis mendapatkan akses ke seluruh server pusat bank.", "Manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank.", "Karena sistem keamanan m-banking di Indonesia belum memiliki enkripsi pelindung sama sekali.", "Karena penipu tidak memiliki komputer yang cukup canggih untuk melakukan peretasan sistem."]
    random.shuffle(opsi_m1)
    st.session_state.list_opsi_m1 = opsi_m1

if "list_opsi_m2" not in st.session_state:
    opsi_m2 = ["Segera klik tautan tersebut untuk memverifikasi data sebelum batas waktu habis agar saldo aman.", "Membalas SMS tersebut dengan kata-kata kasar untuk menakut-nakuti penipu.", "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.", "Mentransfer seluruh saldo ke rekening saudara agar tidak bisa disedot oleh sistem bank."]
    random.shuffle(opsi_m2)
    st.session_state.list_opsi_m2 = opsi_m2

if "list_opsi_m3" not in st.session_state:
    opsi_m3 = ["Melihat apakah ada lambang centang hijau di dalam foto profil akun WhatsApp tersebut.", "Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan.", "Mengecek apakah nomor WhatsApp tersebut menggunakan kode telepon luar negeri atau lokal.", "Mengukur tingkat keramahan bahasa chat yang digunakan oleh admin CS tersebut."]
    random.shuffle(opsi_m3)
    st.session_state.list_opsi_m3 = opsi_m3

if "list_opsi_m4" not in st.session_state:
    opsi_m4 = ["Mengikuti arahannya untuk mengaktifkan Paylater demi menyelamatkan anak yang sedang ditahan polisi.", "Meminta keringanan harga uang damai agar tidak perlu mencairkan utang paylater terlalu besar.", "Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater.", "Datang ke kantor polisi terdekat sendirian tanpa mencoba menghubungi anak terlebih dahulu."]
    random.shuffle(opsi_m4)
    st.session_state.list_opsi_m4 = opsi_m4

if "list_opsi_m5" not in st.session_state:
    opsi_m5 = ["Segera menginstal file APK tersebut agar bisa melihat foto bukti pelanggaran sebelum nomor STNK diblokir polisi.", "Menolak menginstal file tersebut, langsung menghapus pesan, and memeriksa status tilang secara mandiri melalui situs resmi ETLE Korlantas Polri menggunakan nomor pelat kendaraan.", "Mengirimkan file APK tersebut ke grup WhatsApp keluarga untuk menanyakan apakah filenya aman atau tidak.", "Mentransfer sejumlah uang damai yang diminta ke rekening pengirim pesan agar urusan hukum cepat selesai."]
    random.shuffle(opsi_m5)
    st.session_state.list_opsi_m5 = opsi_m5

if "list_opsi_m6" not in st.session_state:
    opsi_m6 = ["Langsung mengunduh dan menginstal file APK Detail Denda Pajak agar toko online Anda tidak disita oleh kantor pajak.", "Membalas chat tersebut dengan mengirimkan foto KTP dan NPWP toko untuk membuktikan bahwa Anda taat pajak.", "Menghapus pesan tersebut dan mengabaikannya, karena instansi pajak resmi tidak pernah mengirimkan dokumen penagihan denda atau detail pajak dalam format aplikasi APK lewat WhatsApp pribadi.", "Datang ke kantor pajak dengan membawa HP yang sudah menginstal file APK tersebut untuk meminta penjelasan."]
    random.shuffle(opsi_m6)
    st.session_state.list_opsi_m6 = opsi_m6

if "list_opsi_m7" not in st.session_state:
    opsi_m7 = [
        "Mengeklik dan menginstal file APK surat panggilan agar tahu jadwal sidang tindak pidana yang dituduhkan.",
        "Mengabaikan pesan WhatsApp tersebut dan memblokir nomornya, karena surat panggilan sidang resmi selalu dikirim melalui surat fisik pos tercatat ke alamat rumah.",
        "Menelepon nomor pengirim dan memohon-mohon agar nama Anda dihapus dari berkas perkara kejaksaan.",
        "Mentransfer uang jaminan ke nomor rekening yang tertera di pesan agar status tersangka dibatalkan."
    ]
    random.shuffle(opsi_m7)
    st.session_state.list_opsi_m7 = opsi_m7

if "list_opsi_m8" not in st.session_state:
    opsi_m8 = [
        "Mengikuti instruksi pelaku dengan memberikan kode verifikasi OTP yang masuk via SMS agar toko tidak ditutup.",
        "Mengirimkan foto buku tabungan dan kartu ATM toko kepada admin WhatsApp tersebut sebagai syarat pembukaan suspensi.",
        "Keluar dari chat WhatsApp tersebut, lalu membuka aplikasi atau website resmi Seller Center marketplace secara mandiri untuk mengecek status toko yang sebenarnya.",
        "Menutup toko online selamanya karena takut aset digital Anda diambil alih oleh sindikat peretas internasional."
    ]
    random.shuffle(opsi_m8)
    st.session_state.list_opsi_m8 = opsi_m8

if "list_opsi_m9" not in st.session_state:
    opsi_m9 = [
        "Segera mengeklik tautan pribadi tersebut untuk mengamankan uang toko online Anda ke rekening asing.",
        "Mengabaikan pesan hoaks tersebut, tidak ikut menyebarkannya, dan mengecek kebenaran informasi melalui situs resmi Bank Indonesia atau portal berita nasional yang terpercaya.",
        "Ikut membagikan kembali pesan tersebut ke grup WhatsApp UMKM lain agar sesama pedagang bisa waspada.",
        "Mendatangi mesin ATM terdekat dengan panik dan menarik seluruh uang tunai tanpa memeriksa kebenaran berita."
    ]
    random.shuffle(opsi_m9)
    st.session_state.list_opsi_m9 = opsi_m9


# =========================================================================
# 🧭 SIDEBAR NAVIGASI TERPADU (MUNCUL SELAMANYA SEBELUM & SESUDAH LOGIN)
# =========================================================================
import os

# 1. Menampilkan Logo di Posisi Paling Atas Terluar Samping
if os.path.exists("logo.png"):
    col_k1, col_tengah, col_k2 = st.sidebar.columns(3)
    with col_tengah:
        st.image("logo.png", use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0px;'>🛡️</h2>", unsafe_allow_html=True)

# 2. Menampilkan Judul Menu di Bawah Gambar Logo
st.sidebar.markdown("<h4 style='text-align: center; margin-top: -10px; font-weight: bold;'>🛡️ GardaDigital</h4>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# 3. 👉 MENU PILIHAN MODUL (DIKELUARKAN AGAR TETAP MUNCUL SETELAH LOGIN)
modul_terpilih = st.sidebar.selectbox(
    "Pilih Modul Pelatihan:",
    [
        "Modul 1: Social Engineering (Gratis)",
        "Modul 2: Digital Phishing & Link Palsu (🔒 Premium)",
        "Modul 3: Mengunci Brankas & Aset Bisnis (🔒 Premium)",
        "Modul 4: Sertifikasi & Manajemen Krisis (🔒 Premium)"
    ]
)

# 4. Tombol Kembali ke Beranda Utama (Hanya aktif jika sudah login)
if st.session_state.login_sukses:
    if st.sidebar.button("🏠 Kembali ke Beranda Utama", use_container_width=True):
        st.session_state.halaman_sekarang = 0
        st.rerun()

st.sidebar.markdown("---")

# 5. Sistem Status Informasi Akun Pengguna
if st.session_state.login_sukses:
    st.sidebar.write(f"👤 Akun Aktif:\n**{st.session_state.user_email}**")
    st.sidebar.write("")
    if st.sidebar.button("🚪 Keluar Akun (Log Out)", use_container_width=True):
        st.session_state.login_sukses = False
        st.session_state.user_email = ""
        st.session_state.halaman_sekarang = 0
        st.session_state.jawaban_user = {}
        st.session_state.materi_selesai = set()
        st.session_state.pilihan_text_save = {}
        st.rerun()
else:
    st.sidebar.write("🔒 Status: Silakan Masuk")
st.sidebar.markdown("---")

# =========================================================================
# 🔒 FILTER KUNCI MODUL PREMIUM (BERLAKU GLOBAL)
# =========================================================================
if "Modul 1" not in modul_terpilih:
    st.markdown(f"### 🔒 Akses Terkunci: {modul_terpilih}")
    st.error("Maaf, modul ini masuk ke dalam paket materi lanjutan (Premium member).")
    st.write("Tingkatkan pertahanan bisnis Anda ke tingkat ahli untuk mempelajari cara membaca *Link Phishing Palsu*, mengunci keamanan *WhatsApp Toko*, dan mengunduh *Sertifikat Kelulusan Resmi Toko*.")
    st.markdown("---")
    st.write("👉 **Hubungi kami via WhatsApp di bawah ini untuk membuka seluruh materi (Hanya Rp 50.000):**")
    st.button("Ajukan Kode Pembuka Akses via Email/WhatsApp", use_container_width=True)
    st.stop() # Menghentikan pembacaan kode bawah jika user memilih modul premium yang terkunci


# =========================================================================
# 🏛️ INTERFACE UTAMA: GERBANG AUTH VS ISI KURIKULUM BATCH
# =========================================================================
if not st.session_state.login_sukses:
    st.markdown("## 🛡️ GardaDigital")
    st.markdown("<p style='color: #BDC3C7; font-size: 15px;'>Security Awareness Training untuk Pelaku UMKM, SOHO, & Personal Awareness</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Masuk Aplikasi", "✍️ Buat Akun Baru"])
    
    with tab1:
        st.subheader("Silakan Masuk ke Akun Anda")
        email_login = st.text_input("Masukkan Email Akun (Gmail):", key="email_l").strip()
        pass_login = st.text_input("Masukkan Password Anda:", type="password", key="pass_l")
        if st.button("Masuk (Login) 🚀", type="primary", use_container_width=True):
            if email_login == "" or pass_login == "":
                st.error("❌ Baris email dan password tidak boleh dikosongkan!")
            else:
                conn = hubungkan_db()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pengguna WHERE email = ? AND password = ?", (email_login, pass_login))
                user = cursor.fetchone()
                conn.close()
                if user:
                    st.session_state.login_sukses = True
                    st.session_state.user_email = email_login
                    
                    # 👉 KUNCI PENGINGAT: Ambil nomor halaman terakhir dari memori database SQLite!
                    conn = hubungkan_db()
                    cursor = conn.cursor()
                    cursor.execute("SELECT halaman_terakhir FROM pengguna WHERE email = ?", (email_login,))
                    halaman_db = cursor.fetchone()
                    conn.close()
                    
                    # Jika user sudah pernah belajar sampai halaman tertentu, langsung lempar ke halaman tersebut!
                    if halaman_db and halaman_db[0] > 0:
                        st.session_state.halaman_sekarang = halaman_db[0]
                    else:
                        st.session_state.halaman_sekarang = 0 # Lempar ke beranda jika beneran akun baru
                        
                    st.success("✅ Login Berhasil! Memulihkan rekam jejak pelatihan Anda...")
                    st.rerun()

                else:
                    st.error("❌ Email atau password salah!")

    with tab2:
        st.subheader("Registrasi Akun Anggota Baru")
        email_reg = st.text_input("Buat Email Baru (Gmail):", key="email_r").strip()
        pass_reg = st.text_input("Buat Password Akun:", type="password", key="pass_r")
        if st.button("Daftar Akun Baru 📝", use_container_width=True):
            if email_reg == "" or pass_reg == "":
                st.error("❌ Baris pendaftaran tidak boleh ada yang kosong!")
            elif "@" not in email_reg:
                st.error("❌ Format penulisan wajib menggunakan alamat email yang valid!")
            else:
                conn = hubungkan_db()
                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO pengguna (email, password) VALUES (?, ?)", (email_reg, pass_reg))
                    conn.commit()
                    st.success("🎉 Akun berhasil dibuat! Silakan login di tab sebelah.")
                except sqlite3.IntegrityError:
                    st.error("🚨 Email ini sudah terdaftar!")
                finally:
                    conn.close()

# ----------------- KONDISI KETIKA USER SUDAH LOGIN SUKSES -----------------
else:
    # --- HALAMAN 0: BERANDA UTAMA ---
    if st.session_state.halaman_sekarang == 0:
        st.markdown("<h1 style='text-align: center;'>🛡️ GardaDigital</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #BDC3C7;'>Security Awareness Training untuk Pelaku UMKM, SOHO, & Personal Awareness</p>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #F1C40F; font-style: italic;'>\"Membangun Perisai Siber Akal Sehat, Melindungi Aset Toko & Rekening Tabungan Anda.\"</h4>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.write(f"👋 **Selamat Datang Kembali, {st.session_state.user_email}!**")
        st.write("Sistem kuis linear GardaDigital versi super solid telah aktif. Pelatihan Modul 1 ini dipecah menjadi beberapa **Batch Evaluasi** demi kenyamanan belajar Anda.")
        
        st.write("")
        if st.button("🚀 Mulai Petualangan Pelatihan", type="primary", use_container_width=True):
            # 👉 KUNCI PENGINGAT DI BERANDA: Ambil data halaman terakhir dari database saat tombol diklik!
            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("SELECT halaman_terakhir FROM pengguna WHERE email = ?", (st.session_state.user_email,))
            halaman_db = cursor.fetchone()
            conn.close()
            
            # Logika Lompat Pintar: Jika user sudah punya riwayat halaman, langsung terbangkan ke sana!
            if halaman_db and halaman_db[0] > 0:
                st.session_state.halaman_sekarang = halaman_db[0]
            else:
                # Jika benar-benar akun baru yang belum punya riwayat, arahkan normal ke halaman Intro Teori
                st.session_state.halaman_sekarang = 1
                
            st.rerun()


    # --- HALAMAN 1: GERBANG PENGENALAN ---
    elif st.session_state.halaman_sekarang == 1:
        st.markdown("## 🧠 Apa itu Social Engineering? (Penjelasan untuk Awam)")
        st.markdown("---")
        st.write("Bayangkan Anda memiliki rumah dengan gembok anti-maling seharga 5 juta dan dipasang kamera CCTV di setiap sudutnya. Rumah itu adalah **Sistem Perbankan atau Marketplace** Anda.")
        st.write("Maling biasa akan menyerah mencoba membobol pagar besi tersebut. Namun, maling yang cerdas tidak akan menyentuh gembok Anda. Dia akan menyamar menjadi Kurir Paket fiktif, mengetuk pintu Anda, lalu berkata: *'Permisi Ibu, ada paket darurat dari keluarga di desa, tolong pinjam kunci pagarnya sebentar untuk memasukkan barang.'* Karena kasihan, Anda memberikan kunci itu secara sukarela.")
        st.success("💡 **Itulah Social Engineering (Rekayasa Sosial).** Peretas tidak membobol sistem komputer Bank yang berlapis baja. Mereka memilih **meretas Akal Sehat dan Emosi Manusia** (seperti rasa panik, takut, atau serakah) agar korban menyerahkan kunci rahasianya (PIN, OTP, atau Password) sendiri tanpa paksaan.")
        st.markdown("---")
        if st.button("Masuk ke Studi Kasus 1 ➡️", type="primary", use_container_width=True):
            st.session_state.halaman_sekarang = 2
            st.rerun()

        # --- JALUR ENGINE MULTI-MATERI BER-SENSOR SAKTI (MATERI 1 SAMPAI 6) ---
    # 👉 KUNCI PERBAIKAN SINTAKS: Memasukkan daftar halaman kuis materi yang menggunakan mesin sensor kotak hitam
    elif (2 <= st.session_state.halaman_sekarang <= 5) or (st.session_state.halaman_sekarang in [7, 8, 9, 10, 12]):
        if st.session_state.halaman_sekarang == 2:
            mid, nomor, judul = "m1", 1, "Materi 1: Pengenalan Social Engineering (Sistem vs Manusia)"
            isi_teks = "Siti menerima pesan WhatsApp dari nomor tidak dikenal menggunakan profil e-commerce resmi menyatakan akun tokonya akan dibekukan permanen dalam 10 menit karena audit fiktif. Karena panik, Siti memasukkan kode rahasia SMS-nya ke link palsu yang diberikan. Dalam 3 menit, saldo penjualannya ludes dikuras."
            tips_teks = "Jika menerima pesan yang memicu emosi ekstrem (sangat panik/sangat senang), logika Anda sedang dilumpuhkan. Diamkan pesan itu selama 10 menit agar otak kembali tenang."
            soal_teks = "Mengapa pelaku penipuan digital lebih sering mengincar korban manusia secara langsung dibandingkan membobol sistem pertahanan server perbankan/marketplace?"
            opsi_sidang = st.session_state.list_opsi_m1
            next_hal = 3
        
        elif st.session_state.halaman_sekarang == 3:
            mid, nomor, judul = "m2", 2, "Materi 2: Ancaman Pemblokiran Rekening & E-Wallet (Modus Urgency)"
            isi_teks = "Pak Budi katering menerima SMS tengah malam menyatakan rekeningnya diblokir dan jika tidak melakukan konfirmasi tarif di link bca-pembatalan-tarif-dana.com dalam waktu 2 jam, saldo modal belanjanya akan hangus. Pak Budi panik, klik link tersebut, dan menyerahkan data PIN-nya ke website tiruan."
            tips_teks = "Bank resmi tidak pernah menggunakan nomor handphone biasa (+62...) untuk mengirimkan notifikasi pemblokiran akun lewat jalur SMS pribadi nasabah."
            soal_teks = "Anda menerima SMS dari nomor handphone biasa: 'AKUN BANK ANDA DIBLOKIR. Untuk mengaktifkan kembali, silakan verifikasi data Anda di bca-validasi-data.com.' Apa tindakan paling tepat?"
            opsi_sidang = st.session_state.list_opsi_m2
            next_hal = 4
        elif st.session_state.halaman_sekarang == 4:
            mid, nomor, judul = "m3", 3, "Materi 3: Fake CS - Akun WhatsApp Tiruan Berlogo Centang Hijau Palsu"
            isi_teks = "Pak Budi melakukan chat dengan nomor CS bank gadungan di internet. Akun tersebut menipu dengan menempelkan gambar lingkaran centang hijau kecil di dalam foto profil bulatannya agar korban percaya. Pak Budi terkecoh dan menyerahkan nomor OTP perbankannya karena mengira akun itu terverifikasi asli."
            tips_teks = "Akun resmi WhatsApp yang memiliki lencana centang hijau asli, lambang centangnya akan selalu berada di sebelah kanan nama profil akun, bukan diedit menyatu di dalam foto profil bulatan."
            soal_teks = "Bagaimana cara paling akurat untuk membedakan antara akun Customer Service bank resmi dengan akun CS penipu di platform WhatsApp?"
            opsi_sidang = st.session_state.list_opsi_m3
            next_hal = 5

        elif st.session_state.halaman_sekarang == 5:
            mid, nomor, judul = "m4", 4, "Materi 4: Vishing - Telepon Darurat Polisi Palsu & Jebakan Kuras Paylater"
            isi_teks = "Pelaku menelepon, membentak mengaku Polisi menyatakan anak korban ditangkap perkara narkoba dan menuntut tebusan 5 juta dalam 15 menit. Saat korban mengaku tabungan kosong, pelaku mendikte korban lewat telepon untuk mengaktifkan limit Paylater di Shopee/Gojek dan mencairkannya langsung ke dompet digital pelaku."
            tips_teks = "Institusi kepolisian resmi tidak pernah meminta uang damai tebusan perkara lewat telepon, dan tidak ada polisi yang menyuruh warga mengaktifkan dana utang Paylater."
            soal_teks = "Seseorang menelepon Anda mengaku sebagai Polisi, menyatakan anak Anda ditangkap. Dia meminta Rp 5 Juta. Saat Anda bilang tidak punya uang, dia membimbing Anda untuk membuka aplikasi belanja dan mengaktifkan limit Paylater untuk ditransfer ke dia. Tindakan Anda?"
            opsi_sidang = st.session_state.list_opsi_m4
            next_hal = 6  # Ke halaman Rapor Batch 1

        elif st.session_state.halaman_sekarang == 7:
            mid, nomor, judul = "m5", 5, "Materi 5: Bahaya File .APK Kurir - Modus Berkedok Foto Tilang ETLE"
            isi_teks = "Soni sedang mengendarai motor, mendapatkan pesan WhatsApp dari nomor asing berfoto profil Polantas menyatakan terekam kamera ETLE melanggar marka jalan. Dia dipaksa menginstal berkas Surat_Tilang_Digital.apk untuk melihat bukti foto agar STNK tidak diblokir. Karena ketakutan, Soni menginstal file tersebut, menyebabkan malware menyadap isi SMS OTP perbankannya dan menguras tabungan."
            tips_teks = "Pihak Kepolisian RI tidak pernah mengirimkan berkas tilang dalam format APK lewat WhatsApp. Surat resmi selalu berbentuk fisik yang diantar pos tercatat ke rumah."
            soal_teks = "Anda mendapatkan chat WhatsApp dari nomor pribadi menggunakan foto profil Polantas, melampirkan berkas bernama 'Surat_Tilang_Digital.apk'. Tindakan paling tepat?"
            opsi_sidang = st.session_state.list_opsi_m5
            next_hal = 8
        elif st.session_state.halaman_sekarang == 8:
            mid, nomor, judul = "m6", 6, "Materi 6: Penipuan Korporasi Pajak - Jebakan File APK Denda Ditjen Pajak"
            isi_teks = "Lani staf admin keuangan katering menerima chat mengaku petugas pajak DJP menyatakan tokonya ada denda Rp12.500.000 and mengancam menyita aset toko jika tidak menginstal file Detail_Denda_Pajak_Toko.apk untuk tanda tangan digital. Lani takut, klik instal, and HP operasional kantor diretas menyadap data keuangan m-banking."
            tips_teks = "Instansi pajak resmi selalu menggunakan surat pos atau email domain resmi '@pajak.go.id', tidak pernah menggunakan file aplikasi APK via nomor WA pribadi."
            soal_teks = "Seseorang menghubungi nomor kantor Anda mengaku petugas Ditjen Pajak, melampirkan file 'Detail_Denda_Pajak.apk' and mengancam menyita toko. Tindakan Anda?"
            opsi_sidang = st.session_state.list_opsi_m6
            next_hal = 9 

        # ----------------- HALAMAN 10: MATERI 7 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 9:
            mid, nomor, judul = "m7", 7, "Materi 7: Modus Ketakutan Hukum - Surat Panggilan Sidang Kejaksaan APK"
            isi_teks = "Seorang wiraswasta menerima WhatsApp dari nomor tidak dikenal berlogo Kejaksaan Agung RI. Isinya menyatakan nama korban terseret sebagai saksi kunci kasus tindak pidana korupsi pencucian uang. Korban dipaksa mengunduh file berkas bernama 'Surat_Panggilan_Sidang_Kejaksaan.apk' untuk melihat rincian kasus dan ruangan sidang di pengadilan negeri besok pagi. Karena syok dan takut ditangkap hukum, korban langsung menginstal file tersebut. Aplikasi tiruan itu langsung mengambil alih kendali HP dan mencuri seluruh data rahasia perbankannya."
            tips_teks = "Kejaksaan atau Pengadilan resmi tidak pernah memanggil saksi atau tersangka menggunakan file aplikasi Android berformat APK via chat WhatsApp pribadi."
            soal_teks = "Anda menerima pesan WhatsApp yang melampirkan berkas 'Surat_Panggilan_Sidang_Kejaksaan.apk' dan menyatakan Anda terseret kasus pidana. Tindakan perlindungan siber Anda?"
            opsi_sidang = st.session_state.list_opsi_m7
            next_hal = 10  # Jembatan lompat menuju Materi 8 besok

        # ----------------- HALAMAN 11: MATERI 8 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 10:
            mid, nomor, judul = "m8", 8, "Materi 8: Ancaman Merchant - Manipulasi Chat Suspensi Akun Admin Toko"
            isi_teks = "Seorang admin toko online di marketplace menerima chat WhatsApp dari nomor pribadi yang memasang foto logo pusat bantuan merchant. Pelaku menyatakan toko online korban terdeteksi melakukan pelanggaran berat dan akan dinonaktifkan selamanya dalam waktu 15 menit, kecuali admin melakukan verifikasi pembatalan lewat aplikasi 'Verifikasi_Merchant_Seller.apk' yang dilampirkan. Admin yang panik memikirkan nasib mata pencahariannya langsung mengklik tombol instal, mengantarkan token login tokonya jatuh ke tangan sindikat peretas dan menguras saldo penjualan."
            tips_teks = "Pihak marketplace resmi selalu mengirimkan notifikasi penalti atau pembatasan akun secara internal langsung di dalam menu pemberitahuan aplikasi dasbor seller center resmi, bukan nomor WhatsApp pribadi."
            soal_teks = "Toko online Anda menerima pesan WhatsApp dari nomor asing menyatakan toko Anda akan ditutup permanen dalam 15 menit, dan meminta Anda menginstal file 'Verifikasi_Merchant_Seller.apk'. Tindakan paling aman?"
            opsi_sidang = st.session_state.list_opsi_m8
            next_hal = 11  # Pintu masuk menuju Halaman Rapor Akhir Batch 2 Final!

        # ----------------- HALAMAN 12: MATERI 9 (BATCH 3 START - TEMA HOAKS!) -----------------
        elif st.session_state.halaman_sekarang == 12:
            mid, nomor, judul = "m9", 9, "Materi 9: Manipulasi Informasi Massa - Isu Hoaks Finansial & Rush Dollar"
            isi_teks = "Seorang pelaku usaha SOHO menerima pesan berantai di grup WhatsApp keluarga yang memuat potongan video berita editan dengan narasi bombastis: *'PENGUMUMAN DARURAT ATURAN NEGARA. Kondisi perbankan nasional kritis, segera cairkan seluruh dana tabungan Anda di ATM dalam 24 jam sebelum aset disita negara (Gerakan Rush Dollar).'* Korban yang panik luar biasa langsung mencoba masuk ke aplikasi m-banking-nya. Di saat bersamaan, penipu mengirimkan chat pribadi berkedok tautan penyelamatan data: *'bca-pencairan-cepat.com'*. Karena logikanya lumpuh akibat hoaks massal tersebut, korban memindahkan seluruh saldo usahanya ke rekening penipu."
            tips_teks = "Isu finansial nasional atau kebijakan darurat negara selalu disiarkan resmi melalui stasiun televisi nasional, siaran pers Sekretariat Negara, atau situs resmi berdomain '.go.id'. Jangan pernah mengambil keputusan keuangan instan berdasarkan pesan berantai WhatsApp grup."
            soal_teks = "Anda menerima pesan berantai di grup WhatsApp bahwa bank tempat Anda menyimpan modal usaha akan bangkrut dan mendesak warga menarik uang secara massal, diikuti chat pribadi yang memberikan link pemindahan saldo aman. Tindakan paling bijak?"
            opsi_sidang = st.session_state.list_opsi_m9
            next_hal = 13  # Pintu masuk menuju Materi 10 selanjutnya


        st.markdown(f"### 📘 {judul}")
        st.write(isi_teks)
        st.info(f"💡 **Trik Lapangan:** {tips_teks}")
        st.markdown("---")
        st.subheader(f"✍️ UJIAN MANDIRI MATERI {nomor}")
        st.write(soal_teks)

        terkunci = mid in st.session_state.materi_selesai

        # 🛠️ ENGINE SENSOR ANTI-CHEAT KOTAK HITAM KONSISTEN
        opsi_tampilan = []
        for o in opsi_sidang:
            if terkunci:
                opsi_tampilan.append("".join(["█" if huruf != " " else " " for huruf in o]))
            else:
                opsi_tampilan.append(o)

        index_default = None
        if terkunci and st.session_state.pilihan_text_save.get(mid) in opsi_sidang:
            index_default = opsi_sidang.index(st.session_state.pilihan_text_save.get(mid))

        pilihan_user = st.radio("Pilih kalimat jawaban paling tepat di bawah ini:", opsi_tampilan, index=index_default, disabled=terkunci, key=f"radio_{mid}")

        if pilihan_user and not terkunci:
            if st.button("Kunci Jawaban", key=f"btn_{mid}", use_container_width=True, type="primary"):
                st.session_state.materi_selesai.add(mid)
                posisi_klik = opsi_tampilan.index(pilihan_user)
                st.session_state.jawaban_user[mid] = opsi_sidang[posisi_klik]
                st.session_state.pilihan_text_save[mid] = opsi_sidang[posisi_klik]
                st.rerun()

        if terkunci:
            st.warning("🔒 Pilihan teks jawaban di atas otomatis dikunci dan DISENSOR TOTAL oleh sistem.")
            if st.session_state.jawaban_user.get(mid) == KUNCI_MATERI[mid]:
                st.success("✅ **BENAR!** Jawaban Anda sangat tepat. Insting keamanan digital Anda berfungsi sempurna.")
            else:
                st.error("❌ **SALAH!** Anda terjebak rekayasa sosial pelaku.")
            
            teks_lanjut = f"Materi Selanjutnya (Materi {nomor + 1}) ➡️" if nomor != 4 and nomor != 8 else ("Buka Halaman Rapor Batch 1 📊" if nomor == 4 else "Buka Halaman Rapor Batch 2 📊")
            if st.button(teks_lanjut, use_container_width=True):
                # 👉 KUNCI PENGINGAT: Catat halaman baru ke database sebelum berpindah halaman!
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET halaman_terakhir = ? WHERE email = ?", (next_hal, st.session_state.user_email))
                conn.commit()
                conn.close()
                
                st.session_state.halaman_sekarang = next_hal
                st.rerun()


        # ----------------- HALAMAN 6: GERBANG RAPOR EVALUASI BATCH 1 (SUPER BERSIH) -----------------
    elif st.session_state.halaman_sekarang == 6:
        st.markdown("### 📊 Rapor Evaluasi: Pembatasan Batch 1 (Materi 1 - 4)")
        st.write("Sistem menganalisis tingkat ketahanan siber Anda pada 4 materi dasar sebelum mengizinkan Anda melaju ke rumpun materi dokumen APK.")
        
        # Hitung skor secara dinamis
        skor_b1 = 0
        if st.session_state.jawaban_user.get("m1") == KUNCI_MATERI["m1"]: skor_b1 += 1
        if st.session_state.jawaban_user.get("m2") == KUNCI_MATERI["m2"]: skor_b1 += 1
        if st.session_state.jawaban_user.get("m3") == KUNCI_MATERI["m3"]: skor_b1 += 1
        if st.session_state.jawaban_user.get("m4") == KUNCI_MATERI["m4"]: skor_b1 += 1
        
        salah_b1 = 4 - skor_b1

        # Tarik data remidi riil dari database SQLite
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT remidi_b1 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        total_remidi_b1 = data_remidi[0] if data_remidi else 0

        st.metric("Jumlah Upaya Percobaan Batch 1", f"{total_remidi_b1} Kali")
        st.markdown("---")

        # TAMPILKAN HANYA 1 CHART BESAR DI TENGAH (MENGHAPUS CHART KANAN YANG REDUNDAN)
        col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
        with col_t2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:13px;'>🎯 Grafik Akurasi Jawaban Batch 1</p>", unsafe_allow_html=True)
            fig1, ax1 = plt.subplots(figsize=(3, 3))
            ax1.pie([skor_b1, salah_b1], labels=[f"Aman ({skor_b1})", f"Celah ({salah_b1})"], colors=['#2ECC71', '#E74C3C'], autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax1.axis('equal')  
            fig1.patch.set_facecolor('#1E1E1E')
            ax1.set_facecolor('#1E1E1E')
            st.pyplot(fig1)

        st.markdown("---")
        if skor_b1 == 4:
            st.success("👑 **STATUS BATCH 1: LULUS TOTAL (4/4)**\n\nGerbang kurikulum lanjutan Modul 1 (Kategori Dokumen APK Bahaya) resmi dibuka oleh sistem!")
            if st.button("Maju ke Batch 2: Materi Lanjutan (Materi 5) 🔓🚀", type="primary", use_container_width=True):
                st.session_state.halaman_sekarang = 7
                st.rerun()
        else:
            st.error(f"🚨 **STATUS BATCH 1: WAJIB REMIDI ({skor_b1}/4 BENAR)**\n\nSistem GardaDigital mendeteksi akun Anda masih memiliki celah psikologis. Selesaikan remedial kuis 100% benar untuk melanjutkan!")
            if st.button("🔄 Ulangi Ujian Batch 1 (Urutan Kalimat di-Shuffle Kembali 🎲)", type="primary", use_container_width=True):
                # UPDATE COUNTER REMIDI KE DATABASE SQLITE
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET remidi_b1 = remidi_b1 + 1 WHERE email = ?", (st.session_state.user_email,))
                conn.commit()
                conn.close()
                
                for mid in ["m1", "m2", "m3", "m4"]:
                    if mid in st.session_state.materi_selesai: st.session_state.materi_selesai.remove(mid)
                    if mid in st.session_state.jawaban_user: del st.session_state.jawaban_user[mid]
                    if mid in st.session_state.pilihan_text_save: del st.session_state.pilihan_text_save[mid]
                
                random.shuffle(st.session_state.list_opsi_m1)
                random.shuffle(st.session_state.list_opsi_m2)
                random.shuffle(st.session_state.list_opsi_m3)
                random.shuffle(st.session_state.list_opsi_m4)
                st.session_state.halaman_sekarang = 2
                st.rerun()


        # ----------------- HALAMAN 11: RAPOR AKHIR BATCH 2 (KOMULATIF & COCOK DATABASE) -----------------
    elif st.session_state.halaman_sekarang == 11:
        st.markdown("### 📊 Rapor Akhir Evaluasi: Hasil Komulatif (Materi 1 - 8)")
        st.write("Selamat! Anda telah merampungkan 8 materi dasar. Berikut adalah analisis total ketahanan siber komulatif Anda:")
        
        # 1. HITUNG SKOR KOMULATIF NYATA (TOTAL DARI 8 MATERI)
        skor_komulatif = 0
        for m_id in ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8"]:
            if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]:
                skor_komulatif += 1
        
        salah_komulatif = 8 - skor_komulatif

        # 2. AMBIL DATA TOTAL REMIDI USER LANGSUNG DARI DATABASE SQLITE
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT remidi_b1, remidi_b2 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        
        total_remidi_b1 = data_remidi[0] if data_remidi else 0
        total_remidi_b2 = data_remidi[1] if data_remidi else 0

        # Menampilkan metrik data percobaan riil yang tidak akan hilang saat di-refresh
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Percobaan Remidi Batch 1", f"{total_remidi_b1} Kali")
        with col_m2:
            st.metric("Percobaan Remidi Batch 2", f"{total_remidi_b2} Kali")

        st.markdown("---")

        # 3. VISUALISASI SATU PIE CHART BESAR DI TENGAH (MENGAPUS CHART KANAN YANG TIDAK BERGUNA)
        col_tengah1, col_tengah2, col_tengah3 = st.columns([1, 2, 1])
        with col_tengah2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🎯 Grafik Akurasi Komulatif (Materi 1 - 8)</p>", unsafe_allow_html=True)
            fig_final, ax_final = plt.subplots(figsize=(3, 3))
            ax_final.pie([skor_komulatif, salah_komulatif], labels=[f"Aman ({skor_komulatif})", f"Celah ({salah_komulatif})"], colors=['#2ECC71', '#E74C3C'], autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax_final.axis('equal')  
            fig_final.patch.set_facecolor('#1E1E1E')
            ax_final.set_facecolor('#1E1E1E')
            st.pyplot(fig_final)

        st.markdown("---")
        
        # 4. LOGIKA KELULUSAN KOMULATIF MUTLAK
        if skor_komulatif == 8:
            st.success(f"👑 **STATUS EVALUASI: LULUS SEMPURNA (8/8 BENAR)**\n\nSelamat, {st.session_state.user_email}! Rekam jejak Anda menunjukkan tingkat kesadaran siber Anda berada di level tertinggi.")
            
            # 👉 PERBAIKAN: Tombol ini sekarang mengunci halaman 12 (Materi 9) ke database secara permanen!
            if st.button("Maju ke Batch 3: Materi Lanjutan (Materi 9) 🔓🚀", type="primary", use_container_width=True):
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                # Mengunci angka 12 (Materi 9) ke brankas database sebelum halaman berpindah
                cursor.execute("UPDATE pengguna SET halaman_terakhir = 12 WHERE email = ?", (st.session_state.user_email,))
                conn.commit()
                conn.close()
                
                st.session_state.halaman_sekarang = 12  # Lompat maju lurus ke lembaran Materi 9
                st.rerun()

        else:
            st.error(f"🚨 **STATUS EVALUASI: WAJIB REMIDI ({skor_komulatif}/8 BENAR)**\n\nSistem mendeteksi Anda masih memiliki celah bahaya. Anda wajib mengulang kuis di Batch 2 yang salah sampai mendapatkan skor komulatif sempurna!")
            
            if st.button("🔄 Ulangi Ujian Khusus Batch 2 (Kalimat di-Shuffle Kembali 🎲)", type="primary", use_container_width=True):
                # 1. UPDATE COUNTER REMIDI KE DATABASE SQLITE
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET remidi_b2 = remidi_b2 + 1 WHERE email = ?", (st.session_state.user_email,))
                conn.commit()
                conn.close()
                
                # 2. BERSIHKAN HANYA STATUS KUNCIAN & DATA JAWABAN (JANGAN HAPUS BRANKAS OPSI NYA!)
                for mid in ["m5", "m6", "m7", "m8"]:
                    if mid in st.session_state.materi_selesai: 
                        st.session_state.materi_selesai.remove(mid)
                    if mid in st.session_state.jawaban_user: 
                        del st.session_state.jawaban_user[mid]
                    if mid in st.session_state.pilihan_text_save: 
                        del st.session_state.pilihan_text_save[mid]
                
                # 3. 👉 KUNCI AMAN: Langsung acak formasinya di tempat tanpa memicu AttributeError
                random.shuffle(st.session_state.list_opsi_m5)
                random.shuffle(st.session_state.list_opsi_m6)
                random.shuffle(st.session_state.list_opsi_m7)
                random.shuffle(st.session_state.list_opsi_m8)
                
                st.session_state.halaman_sekarang = 7  # Balik lurus ke Materi 5
                st.rerun()

