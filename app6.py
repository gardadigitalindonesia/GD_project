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
    conn = sqlite3.connect("gardadigital.db")
    return conn

def buat_tabel_database():
    conn = hubungkan_db()
    cursor = conn.cursor()
    # Membuat tabel pengguna dasar dengan kolom profil lengkap + Nomor HP
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pengguna (
            email TEXT PRIMARY KEY,
            password TEXT,
            nama_depan TEXT,
            nama_belakang TEXT,
            jenis_kelamin TEXT,
            instansi TEXT,
            no_hp TEXT,
            remidi_b1 INTEGER DEFAULT 0,
            remidi_b2 INTEGER DEFAULT 0,
            halaman_terakhir INTEGER DEFAULT 0,
            status_lulus_b1 INTEGER DEFAULT 0,
            status_lulus_b2 INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    
    # SUNTIKAN OTOMATIS KESELAMATAN: Memaksa database lama menambahkan kolom baru tanpa merusak data
    kolom_baru = [
        ("nama_depan", "TEXT"), ("nama_belakang", "TEXT"), 
        ("jenis_kelamin", "TEXT"), ("instansi", "TEXT"), ("no_hp", "TEXT"),
        ("halaman_terakhir", "INTEGER DEFAULT 0"),
        ("status_lulus_b1", "INTEGER DEFAULT 0"), ("status_lulus_b2", "INTEGER DEFAULT 0")
    ]
    for nama_kolom, tipe_data in kolom_baru:
        try:
            cursor.execute(f"ALTER TABLE pengguna ADD COLUMN {nama_kolom} {tipe_data}")
            conn.commit()
        except sqlite3.OperationalError:
            pass  
    conn.close()


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
    "m10": "Menghapus pesan tersebut, tidak mengklik tautan apa pun, and memverifikasi info bantuan sosial secara mandiri melalui situs resmi Cek Bansos Kemensos RI atau dinas sosial setempat.",
    "m11": "Segera keluar dari grup tersebut, mengabaikan tawaran keuntungan yang tidak masuk akal, and tidak mentransfer uang sepeser pun karena itu adalah modus penipuan investasi skema Ponzi.",
    "m12": "Mengabaikan instruksi SMS tersebut dan memblokir nomornya, karena pengumuman resmi pembagian dividen atau urusan saham emiten selalu dikirimkan lewat surat fisik resmi KSEI atau menu keterbukaan informasi aplikasi sekuritas resmi."

}

# =========================================================================
# 🧠 INISIALISASI VARIABEL MEMORI (ANTI-BUG ATTRIBUTERROR)
# =========================================================================
if "login_sukses" not in st.session_state: st.session_state.login_sukses = False
if "user_email" not in st.session_state: st.session_state.user_email = ""
if "halaman_sekarang" not in st.session_state: st.session_state.halaman_sekarang = 0  
if "jawaban_user" not in st.session_state: st.session_state.jawaban_user = {}
if "materi_selesai" not in st.session_state: st.session_state.materi_selesai = set()
if "pilihan_text_save" not in st.session_state: st.session_state.pilihan_text_save = {}
if "intip_rapor_global" not in st.session_state: st.session_state.intip_rapor_global = False

# =========================================================================
# 🎲 ENGINE PENGACAK JAWABAN BERBASIS MEMORI SERVER
# =========================================================================
if "list_opsi_m1" not in st.session_state:
    st.session_state.list_opsi_m1 = ["Karena membobol akun perorangan bisa otomatis mendapatkan akses ke seluruh server pusat bank.", "Manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank.", "Karena sistem keamanan m-banking di Indonesia belum memiliki enkripsi pelindung sama sekali.", "Karena penipu tidak memiliki komputer yang cukup canggih untuk melakukan peretasan sistem."]
    random.shuffle(st.session_state.list_opsi_m1)
if "list_opsi_m2" not in st.session_state:
    st.session_state.list_opsi_m2 = ["Segera klik tautan tersebut untuk memverifikasi data sebelum batas waktu habis agar saldo aman.", "Membalas SMS tersebut dengan kata-kata kasar untuk menakut-nakuti penipu.", "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.", "Mentransfer seluruh saldo ke rekening saudara agar tidak bisa disedot oleh sistem bank."]
    random.shuffle(st.session_state.list_opsi_m2)
if "list_opsi_m3" not in st.session_state:
    st.session_state.list_opsi_m3 = ["Melihat apakah ada lambang centang hijau di dalam foto profil akun WhatsApp tersebut.", "Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan.", "Mengecek apakah nomor WhatsApp tersebut menggunakan kode telepon luar negeri atau lokal.", "Mengukur tingkat keramahan bahasa chat yang digunakan oleh admin CS tersebut."]
    random.shuffle(st.session_state.list_opsi_m3)
if "list_opsi_m4" not in st.session_state:
    st.session_state.list_opsi_m4 = ["Mengikuti arahannya untuk mengaktifkan Paylater demi menyelamatkan anak yang sedang ditahan polisi.", "Meminta keringanan harga uang damai agar tidak perlu mencairkan utang paylater terlalu besar.", "Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater.", "Datang ke kantor polisi terdekat sendirian tanpa mencoba menghubungi anak terlebih dahulu."]
    random.shuffle(st.session_state.list_opsi_m4)
if "list_opsi_m5" not in st.session_state:
    st.session_state.list_opsi_m5 = ["Segera menginstal file APK tersebut agar bisa melihat foto bukti pelanggaran sebelum nomor STNK diblokir polisi.", "Menolak menginstal file tersebut, langsung menghapus pesan, and memeriksa status tilang secara mandiri melalui situs resmi ETLE Korlantas Polri menggunakan nomor pelat kendaraan.", "Mengirimkan file APK tersebut ke grup WhatsApp keluarga untuk menanyakan apakah filenya aman atau tidak.", "Mentransfer sejumlah uang damai yang diminta ke rekening pengirim pesan agar urusan hukum cepat selesai."]
    random.shuffle(st.session_state.list_opsi_m5)
if "list_opsi_m6" not in st.session_state:
    st.session_state.list_opsi_m6 = ["Langsung mengunduh dan menginstal file APK Detail Denda Pajak agar toko online Anda tidak disita oleh kantor pajak.", "Membalas chat tersebut dengan mengirimkan foto KTP dan NPWP toko untuk membuktikan bahwa Anda taat pajak.", "Menghapus pesan tersebut dan mengabaikannya, karena instansi pajak resmi tidak pernah mengirimkan dokumen penagihan denda atau detail pajak dalam format aplikasi APK lewat WhatsApp pribadi.", "Datang ke kantor pajak dengan membawa HP yang sudah menginstal file APK tersebut untuk meminta penjelasan."]
    random.shuffle(st.session_state.list_opsi_m6)
if "list_opsi_m7" not in st.session_state:
    st.session_state.list_opsi_m7 = ["Mengeklik dan menginstal file APK surat panggilan agar tahu jadwal sidang tindak pidana yang dituduhkan.", "Mengabaikan pesan WhatsApp tersebut dan memblokir nomornya, karena surat panggilan sidang resmi selalu dikirim melalui surat fisik pos tercatat ke alamat rumah.", "Menelepon nomor pengirim dan memohon-mohon agar nama Anda dihapus dari berkas perkara kejaksaan.", "Mentransfer uang jaminan ke nomor rekening yang tertera di pesan agar status tersangka dibatalkan."]
    random.shuffle(st.session_state.list_opsi_m7)
if "list_opsi_m8" not in st.session_state:
    st.session_state.list_opsi_m8 = ["Mengikuti instruksi pelaku dengan memberikan kode verifikasi OTP yang masuk via SMS agar toko tidak ditutup.", "Mengirimkan foto buku tabungan dan kartu ATM toko kepada admin WhatsApp tersebut sebagai syarat pembukaan suspensi.", "Keluar dari chat WhatsApp tersebut, lalu membuka aplikasi atau website resmi Seller Center marketplace secara mandiri untuk mengecek status toko yang sebenarnya.", "Menutup toko online selamanya karena takut aset digital Anda diambil alih oleh sindikat peretas internasional."]
    random.shuffle(st.session_state.list_opsi_m8)
if "list_opsi_m9" not in st.session_state:
#if "list_opsi_m9" not in st.session_state:
    st.session_state.list_opsi_m9 = [
        "Segera mengeklik tautan pribadi tersebut untuk mengamankan uang toko online Anda ke rekening asing.",
        "Mengabaikan pesan hoaks tersebut, tidak ikut menyebarkannya, and mengecek kebenaran informasi melalui situs resmi Bank Indonesia atau portal berita nasional yang terpercaya.",
        "Ikut membagikan kembali pesan tersebut ke grup WhatsApp UMKM lain agar sesama pedagang bisa waspada.",
        "Mendatangi mesin ATM terdekat dengan panik dan menarik seluruh uang tunai tanpa memeriksa kebenaran berita."
    ]
    random.shuffle(st.session_state.list_opsi_m9)

if "list_opsi_m10" not in st.session_state:
    st.session_state.list_opsi_m10 = [
        "Langsung membuka tautan tersebut and mengisi formulir pencairan bansos menggunakan nomor rekening toko.",
        "Menghapus pesan tersebut, tidak mengklik tautan apa pun, and memverifikasi info bantuan sosial secara mandiri melalui situs resmi Cek Bansos Kemensos RI atau dinas sosial setempat.",
        "Mentransfer biaya administrasi pencairan bansos sebesar Rp200.000 ke rekening bendahara fiktif.",
        "Menghubungi pengirim chat untuk berterima kasih karena toko UMKM Anda mendapatkan modal gratis."
    ]
    random.shuffle(st.session_state.list_opsi_m10)

if "list_opsi_m11" not in st.session_state:
    st.session_state.list_opsi_m11 = [
        "Mentransfer dana deposit minimal Rp500.000 terlebih dahulu untuk menguji apakah bonus komisi awal benar-benar bisa dicairkan ke rekening toko.",
        "Segera keluar dari grup tersebut, mengabaikan tawaran keuntungan yang tidak masuk akal, and tidak mentransfer uang sepeser pun karena itu adalah modus penipuan investasi skema Ponzi.",
        "Ikut mengajak staf karyawan warung atau saudara terdekat untuk mendaftar agar keuntungan komisi harian berkelompok menjadi semakin besar.",
        "Mencoba mengirimkan nomor kartu ATM and PIN toko kepada admin grup dengan harapan mendapatkan prioritas pencairan dana bonus."
    ]
    random.shuffle(st.session_state.list_opsi_m11)

if "list_opsi_m12" not in st.session_state:
    st.session_state.list_opsi_m12 = [
        "Mengunduh file APK berkas pembagian saham tersebut untuk memastikan berapa total lembar dividen bonus yang menjadi hak usaha Anda.",
        "Mengabaikan instruksi SMS tersebut dan memblokir nomornya, karena pengumuman resmi pembagian dividen atau urusan saham emiten selalu dikirimkan lewat surat fisik resmi KSEI atau menu keterbukaan informasi aplikasi sekuritas resmi.",
        "Membalas SMS penipu dengan melampirkan foto buku tabungan and nomor rekening koran perusahaan untuk proses klaim dana tunai.",
        "Datang ke kantor cabang bank terdekat and meminta teller menginstalkan file aplikasi klaim dividen tersebut di handphone Anda."
    ]
    random.shuffle(st.session_state.list_opsi_m12)


# =========================================================================
# 🧭 SIDEBAR NAVIGASI TERPADU (WHITE LABEL + RAPOR GLOBAL PINTAR)
# =========================================================================
if os.path.exists("logo.png"):
    col_k1, col_tengah, col_k2 = st.sidebar.columns(3)
    with col_tengah: 
        st.image("logo.png", use_container_width=True)
else:
    st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0px;'>🛡️</h2>", unsafe_allow_html=True)

st.sidebar.markdown("<h4 style='text-align: center; margin-top: -10px; font-weight: bold;'>🛡️ GardaDigital</h4>", unsafe_allow_html=True)
st.sidebar.markdown("---")

modul_terpilih = st.sidebar.selectbox("Pilih Modul Pelatihan:", [
    "Modul 1: Social Engineering (Gratis)", 
    "Modul 2: Digital Phishing (🔒 Premium)",
    "Modul 3: Mengunci Brankas Bisnis (🔒 Premium)", 
    "Modul 4: Sertifikasi Akhir Modul (🔒 Premium)"
])

if "Modul 1" not in modul_terpilih:
    st.markdown(f"### 🔒 Akses Terkunci: {modul_terpilih}")
    st.error("Maaf, modul ini masuk ke dalam paket materi lanjutan (Premium member).")
    st.button("Ajukan Kode Pembuka Akses via Email/WhatsApp", use_container_width=True)
    st.stop()

if st.session_state.login_sukses:
    if st.sidebar.button("🏠 Kembali ke Beranda Utama", use_container_width=True):
        st.session_state.intip_rapor_global = False
        st.session_state.halaman_sekarang = 0
        st.rerun()
        
    # 👉 BARU: TOMBOL INTIP RAPOR GLOBAL (BISA DIKLIK KAPAN SAJA)
    if st.sidebar.button("📊 Lihat Rapor Keseluruhan Saya", use_container_width=True):
        st.session_state.intip_rapor_global = True
        st.rerun()

st.sidebar.markdown("---")
# 5. 👉 BARU: DASBOR PROFIL IDENTITAS PREMIUM (MENAMPILKAN NAMA, INSTITUSI, EMAIL, NO HP)
if st.session_state.login_sukses:
    # Tarik data profil lengkap langsung dari brankas database SQLite
    conn = hubungkan_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nama_depan, nama_belakang, instansi, no_hp FROM pengguna WHERE email = ?", (st.session_state.user_email,))
    profil_db = cursor.fetchone()
    conn.close()
    
    # Ambil nilai aman jika data ditemukan
    n_depan = profil_db[0] if profil_db and profil_db[0] else "User"
    n_belakang = profil_db[1] if profil_db and profil_db[1] else ""
    nama_lengkap = f"{n_depan} {n_belakang}".strip()
    institusi_user = profil_db[2] if profil_db and profil_db[2] else "Personal Awareness"
    handphone_user = profil_db[3] if profil_db and profil_db[3] else "-"
    
    # Tampilkan pembungkus kartu visual rapi di sidebar
    st.sidebar.markdown("### 👤 Profil Anggota")
    st.sidebar.markdown(f"**Nama:**\n{nama_lengkap}")
    st.sidebar.markdown(f"**Institusi:**\n{institusi_user}")
    st.sidebar.markdown(f"**Email:**\n`{st.session_state.user_email}`")
    st.sidebar.markdown(f"**No. HP:**\n{handphone_user}")
    st.sidebar.write("")
    
    if st.sidebar.button("🚪 Keluar Akun (Log Out)", use_container_width=True):
        st.session_state.login_sukses = False
        st.session_state.user_email = ""
        st.session_state.halaman_sekarang = 0
        st.session_state.jawaban_user = {}
        st.session_state.materi_selesai = set()
        st.session_state.pilihan_text_save = {}
        st.session_state.intip_rapor_global = False
        st.rerun()

    # 👉 BARU: TOMBOL RESET INSTAN KHUSUS DEVELOPER UNTUK SIMULASI PENGUJIAN JAWABAN
    st.sidebar.markdown("---")
    st.sidebar.markdown("<p style='color: #E74C3C; font-weight: bold; font-size: 12px; margin-bottom: 2px;'>🛠️ PANEL PENGUJIAN DEVELOPER</p>", unsafe_allow_html=True)
    if st.sidebar.button("🔄 Reset Total Riwayat Jawaban", use_container_width=True, type="secondary"):
        # 1. Reset Riwayat Kelulusan and Counter Remidi di Database SQLite untuk Akun Ini
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pengguna 
            SET halaman_terakhir = 0, 
                status_lulus_b1 = 0, 
                status_lulus_b2 = 0, 
                remidi_b1 = 0, 
                remidi_b2 = 0 
            WHERE email = ?
        """, (st.session_state.user_email,))
        conn.commit()
        conn.close()
        
        # 2. Kosongkan Seluruh Memori RAM Jawaban and Kuncian Sensor di Streamlit
        st.session_state.halaman_sekarang = 0
        st.session_state.jawaban_user = {}
        st.session_state.materi_selesai = set()
        st.session_state.pilihan_text_save = {}
        st.session_state.intip_rapor_global = False
        
        # 3. Kocok Ulang Semua Opsi Kuis dari Awal Lagi agar Formasinya Baru 🎲
        random.shuffle(st.session_state.list_opsi_m1)
        random.shuffle(st.session_state.list_opsi_m2)
        random.shuffle(st.session_state.list_opsi_m3)
        random.shuffle(st.session_state.list_opsi_m4)
        random.shuffle(st.session_state.list_opsi_m5)
        random.shuffle(st.session_state.list_opsi_m6)
        random.shuffle(st.session_state.list_opsi_m7)
        random.shuffle(st.session_state.list_opsi_m8)
        random.shuffle(st.session_state.list_opsi_m9)
        random.shuffle(st.session_state.list_opsi_m10)
        random.shuffle(st.session_state.list_opsi_m11)
        random.shuffle(st.session_state.list_opsi_m12)
        
        st.success("🔄 Memori Ujian Berhasil Direset! Akun Anda kembali ke status awal.")
        st.rerun()


else:
    st.sidebar.write("🔒 Status: Silakan Masuk")
st.sidebar.markdown("---")

# =========================================================================
# 🏛️ INTERFACE UTAMA: GERBANG AUTH VS JALUR BELAJAR
# =========================================================================

# 👉 BARU: INTERFAS HALAMAN RAPOR GLOBAL JIKA TOMBOL SIDEBAR DIKLIK
if st.session_state.login_sukses and st.session_state.intip_rapor_global:
    st.markdown("### 📊 Dasbor Progres Rapor Global Anda")
    st.write("Dasbor ini merangkum seluruh rekam jejak progres materi yang Anda selesaikan dari total kurikulum Modul 1.")
    
    total_materi_selesai = len(st.session_state.materi_selesai)
    total_materi_sisa = 20 - total_materi_selesai
    
    st.markdown(f"#### Progress Kelengkapan Kelas: **{total_materi_selesai} dari 20 Materi Selesai**")
    st.progress(total_materi_selesai / 20)
    
    col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
    with col_g2:
        fig_g, ax_g = plt.subplots(figsize=(3, 3))
        ax_g.pie([total_materi_selesai, total_materi_sisa], labels=["Selesai", "Sisa Materi"], colors=['#2ECC71', '#555555'], autopct='%1.0f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
        ax_g.axis('equal')
        fig_g.patch.set_facecolor('#1E1E1E')
        ax_g.set_facecolor('#1E1E1E')
        st.pyplot(fig_g)
        
    st.markdown("---")
    if st.button("⬅️ Kembali Melanjutkan Pembelajaran Materi", type="primary", use_container_width=True):
        st.session_state.intip_rapor_global = False
        st.rerun()
    st.stop()

# ----------------- KONDISI A: PENGGUNA BELUM LOGIN -----------------
if not st.session_state.login_sukses:
    st.markdown("## 🛡️ GardaDigital")
    st.markdown("<p style='color: #BDC3C7; font-size: 15px;'>Security Awareness Training untuk Pelaku UMKM, SOHO, & Personal Awareness</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["🔐 Masuk Aplikasi", "✍️ Buat Akun Baru"])
    
    # --- TAB 1: FORM LOGIN ---
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
                    st.session_state.halaman_sekarang = 0  # Kunci mendarat di beranda dulu
                    st.rerun()
                else:
                    st.error("❌ Email atau password salah!")

        # --- TAB 2: FORMULIR PENDAFTARAN LENGKAP UNTUK SERTIFIKAT DIGITAL ---
    with tab2:
        st.subheader("Registrasi Profil Anggota Baru")
        email_reg = st.text_input("Buat Email Baru (Gmail):", key="email_r").strip()
        pass_reg = st.text_input("Buat Password Akun:", type="password", key="pass_r")
        
        col_n1, col_n2 = st.columns(2)
        with col_n1: 
            nama_depan = st.text_input("Nama Depan (Sesuai KTP):", key="n_depan").strip()
        with col_n2: 
            nama_belakang = st.text_input("Nama Belakang:", key="n_belakang").strip()
        
        j_kelamin = st.selectbox("Jenis Kelamin:", ["Laki-laki", "Perempuan"], key="j_kel")
        nama_instansi = st.text_input("Nama Toko UMKM / Sekolah / Universitas:", key="n_instansi").strip()
        
        # 👉 BARU: INPUT NOMOR HANDPHONE PENGGUNA
        nomor_hp = st.text_input("Masukkan Nomor WhatsApp Aktif (Contoh: 08123456xxx):", key="n_hp").strip()
        
        if st.button("Daftar Akun Baru 📝", use_container_width=True):
            if email_reg == "" or pass_reg == "" or nama_depan == "" or nama_instansi == "" or nomor_hp == "":
                st.error("❌ Mohon lengkapi seluruh formulir profil identitas sertifikat Anda!")
            elif "@" not in email_reg:
                st.error("❌ Format penulisan wajib menggunakan alamat email yang valid!")
            else:
                conn = hubungkan_db()
                cursor = conn.cursor()
                try:
                    # 👉 PERBAIKAN DATABASE: Memasukkan 7 data lengkap termasuk nomor HP
                    cursor.execute("""
                        INSERT INTO pengguna (email, password, nama_depan, nama_belakang, jenis_kelamin, instansi, no_hp)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (email_reg, pass_reg, nama_depan, nama_belakang, j_kelamin, nama_instansi, nomor_hp))
                    conn.commit()
                    st.success("🎉 Akun & Profil Sertifikat berhasil dikunci! Silakan pindah ke tab 'Masuk Aplikasi'.")
                except sqlite3.IntegrityError:
                    st.error("🚨 Email ini sudah terdaftar di database sistem!")
                finally:
                    conn.close()


# ----------------- KONDISI KETIKA USER SUDAH LOGIN SUKSES -----------------
else:
    # --- HALAMAN 0: BERANDA UTAMA ---
    if st.session_state.halaman_sekarang == 0:
        # Menarik sapaan nama asli dari database SQLite
        conn = hubungkan_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nama_depan, jenis_kelamin FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        db_p = cursor.fetchone()
        conn.close()
        
        sapaan = "Bapak/Ibu"
        if db_p and db_p[0]:
            # 👉 PERBAIKAN LOGIKA: Membaca indeks tuple agar sapaan nama asli muncul akurat
            sapaan = ("Bapak " if db_p[1] == "Laki-laki" else "Ibu ") + db_p[0]
            
        st.markdown("<h1 style='text-align: center;'>🛡️ GardaDigital</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #BDC3C7;'>Security Awareness Training untuk Pelaku UMKM, SOHO, & Personal Awareness</p>", unsafe_allow_html=True)
        st.markdown("<h4 style='text-align: center; color: #F1C40F; font-style: italic;'>\"Membangun Perisai Siber Akal Sehat, Melindungi Aset Toko & Rekening Tabungan Anda.\"</h4>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.write(f"👋 **Selamat Datang Kembali, {sapaan}!**")
        st.write("Sistem kuis linear GardaDigital versi super solid telah aktif. Pelatihan Modul 1 ini dipecah menjadi beberapa **Batch Evaluasi** demi kenyamanan belajar Anda.")
        
        st.write("")
        if st.button("🚀 Mulai Petualangan Pelatihan", type="primary", use_container_width=True):
            conn = hubungkan_db()
            cursor = conn.cursor()
            cursor.execute("SELECT halaman_terakhir, status_lulus_b1 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
            data_user = cursor.fetchone()
            conn.close()
            
            if data_user:
                hal_terakhir, b1_lulus = data_user[0], data_user[1]
                if b1_lulus == 1 and hal_terakhir >= 7:
                    st.session_state.halaman_sekarang = hal_terakhir
                elif b1_lulus == 1:
                    st.session_state.halaman_sekarang = 7
                else:
                    st.session_state.halaman_sekarang = hal_terakhir if hal_terakhir > 0 else 1
            else:
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

    # --- JALUR ENGINE MULTI-MATERI BER-SENSOR SAKTI (MATERI 1 SAMPAI 6, 7, 8, 9, 10) ---
    elif (2 <= st.session_state.halaman_sekarang <= 5) or (7 <= st.session_state.halaman_sekarang <= 10) or (12 <= st.session_state.halaman_sekarang <= 15):
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
            isi_teks = "Pak Budi melakukan chat dengan nomor CS bank gadungan di internet. Akun tersebut menipu dengan menempelkan gambar lingkaran centang hijau kecil di dalam foto profil baratannya agar korban percaya. Pak Budi terkecoh dan menyerahkan nomor OTP perbankannya karena mengira akun itu terverifikasi asli."
            tips_teks = "Akun resmi WhatsApp yang memiliki lencana centang hijau asli, lambang centangnya akan selalu berada di sebelah kanan nama profil akun, bukan diedit menyatu di dalam foto profil bulatan."
            soal_teks = "Bagaimana cara paling akurat untuk membedakan antara akun Customer Service bank resmi dengan akun CS penipu di platform WhatsApp?"
            opsi_sidang = st.session_state.list_opsi_m3
            next_hal = 5

        elif st.session_state.halaman_sekarang == 5:
            mid, nomor, judul = "m4", 4, "Materi 4: Vishing - Telepon Darurat Polisi Palsu & Jebakan Kuras Paylater"
            isi_teks = "Pelaku menelepon, membentak mengaku Polisi menyatakan anak korban ditangkap perkara narkoba dan menuntut tebusan 5 juta dalam 15 menit. Saat korban mengaku tabungan kosong, pelaku mendikte korban lewat telepon untuk mengaktifkan limit Paylater di Shopee/Gojek dan mencairkannya langsung ke dompet digital pelaku."
            tips_teks = "Institusi kepolisian resmi tidak pernah meminta uang damai tebusan perkara lewat telepon, dan tidak ada polisi yang menyuruh warga mengaktifkan dana utang Paylater."
            soal_teks = "Seseorang menelepon Anda mengaku sebagai Polisi, menyatakan anak Anda ditangkap. Dia meminta Rp 5 Juta. Saat Anda billing tidak punya uang, dia membimbing Anda untuk membuka aplikasi belanja dan mengaktifkan limit Paylater untuk ditransfer ke dia. Tindakan Anda?"
            opsi_sidang = st.session_state.list_opsi_m4
            next_hal = 6  

        elif st.session_state.halaman_sekarang == 7:
            mid, nomor, judul = "m5", 5, "Materi 5: Bahaya File .APK Kurir - Modus Berkedok Foto Tilang ETLE"
            isi_teks = "Soni sedang mengendarai motor, mendapatkan pesan WhatsApp dari nomor asing berfoto profil Polantas menyatakan terekam kamera ETLE melanggar marka jalan. Dia dipaksa menginstal berkas Surat_Tilang_Digital.apk untuk melihat bukti foto agar STNK tidak diblokir. Karena ketakutan, Soni menginstal file tersebut, menyebabkan malware menyadap isi SMS OTP perbankannya dan menguras tabungan."
            tips_teks = "Pihak Kepolisian RI tidak pernah mengirimkan berkas tilang dalam format APK lewat WhatsApp. Surat resmi selalu berbentuk fisik yang diantar pos tercatat ke rumah."
            soal_teks = "Anda mendapatkan chat WhatsApp dari nomor pribadi menggunakan foto profil Polantas, melampirkan berkas bernama 'Surat_Tilang_Digital.apk'. Tindakan paling tepat?"
            opsi_sidang = st.session_state.list_opsi_m5
            next_hal = 8

        elif st.session_state.halaman_sekarang == 8:
            mid, nomor, judul = "m6", 6, "Materi 6: Penipuan Korporasi Pajak - Jebakan File APK Denda Ditjen Pajak"
            isi_teks = "Lani staf admin keuangan katering menerima chat mengaku petugas pajak DJP menyatakan tokonya ada denda Rp12.500.000 dan mengancam menyita aset toko jika tidak menginstal file Detail_Denda_Pajak_Toko.apk untuk tanda tangan digital. Lani takut, klik instal, and HP operasional kantor diretas menyadap data keuangan m-banking."
            tips_teks = "Instansi pajak resmi selalu menggunakan surat pos atau email domain resmi '@pajak.go.id', tidak pernah menggunakan file aplikasi APK via nomor WA pribadi."
            soal_teks = "Seseorang menghubungi nomor kantor Anda mengaku petugas Ditjen Pajak, melampirkan file 'Detail_Denda_Pajak.apk' dan mengancam menyita toko. Tindakan Anda?"
            opsi_sidang = st.session_state.list_opsi_m6
            next_hal = 9  # Lompat maju lurus ke lembaran Materi 7

        elif st.session_state.halaman_sekarang == 9:
            mid, nomor, judul = "m7", 7, "Materi 7: Modus Ketakutan Hukum - Surat Panggilan Sidang Kejaksaan APK"
            isi_teks = "Seorang wiraswasta menerima WhatsApp dari nomor tidak dikenal berlogo Kejaksaan Agung RI menyatakan nama korban terseret saksi kunci kasus korupsi. Korban dipaksa mengunduh file Surat_Panggilan_Sidang_Kejaksaan.apk untuk melihat jadwal sidang besok pagi. Karena syok, korban langsung menginstal file tersebut. Aplikasi tiruan itu menyadap kendali penuh HP dan mencuri akun finansial."
            tips_teks = "Kejaksaan atau Pengadilan resmi tidak pernah memanggil saksi atau tersangka menggunakan file aplikasi Android berformat APK via chat WhatsApp pribadi."
            soal_teks = "Anda menerima pesan WhatsApp yang melampirkan berkas 'Surat_Panggilan_Sidang_Kejaksaan.apk'. Tindakan perlindungan siber Anda?"
            opsi_sidang = st.session_state.list_opsi_m7
            next_hal = 10

        elif st.session_state.halaman_sekarang == 10:
            mid, nomor, judul = "m8", 8, "Materi 8: Ancaman Merchant - Manipulasi Chat Suspensi Akun Admin Toko"
            isi_teks = "Seorang admin toko online di marketplace menerima chat WhatsApp berlogo bantuan merchant menyatakan toko akan dinonaktifkan dalam 15 menit kecuali mengonfirmasi lewat file Verifikasi_Merchant_Seller.apk yang dilampirkan. Admin panik, klik tombol instal, mengantarkan token login tokonya jatuh ke tangan sindikat peretas."
            tips_teks = "Pihak marketplace resmi selalu mengirimkan notifikasi penalti langsung di dalam menu pemberitahuan aplikasi dasbor seller center resmi, bukan nomor WhatsApp pribadi."
            soal_teks = "Toko online Anda menerima pesan WhatsApp meminta Anda menginstal file 'Verifikasi_Merchant_Seller.apk'. Tindakan paling aman?"
            opsi_sidang = st.session_state.list_opsi_m8
            next_hal = 11

        elif st.session_state.halaman_sekarang == 12:
            mid, nomor, judul = "m9", 9, "Materi 9: Manipulasi Informasi Massa - Isu Hoaks Finansial & Rush Dollar"
            isi_teks = "Seorang pedagang menerima hoaks video berantai di grup WA bahwa perbankan kritis and menyuruh warga menarik uang tunai serentak (Rush Dollar). Di saat bersamaan, penipu mengirim link pribadi bca-pencairan-cepat.com untuk pemindahan saldo aman. Karena panik, korban klik tautan tersebut and menyerahkan saldo tokonya."
            tips_teks = "Isu finansial nasional selalu disiarkan resmi melalui stasiun TV nasional atau situs resmi berdomain '.go.id'. Jangan mengambil keputusan keuangan berdasarkan pesan berantai grup WhatsApp."
            soal_teks = "Anda menerima hoaks berantai Rush Dollar diikuti link klaim pemindahan saldo aman dari nomor asing. Tindakan paling bijak?"
            opsi_sidang = st.session_state.list_opsi_m9
            next_hal = 13  # Pintu jembatan menuju Materi 10 Selanjutnya

        # 👉 BARU: MATERI 10 LENGKAP SIAP COBA
        elif st.session_state.halaman_sekarang == 13:
            mid, nomor, judul = "m10", 10, "Materi 10: Hoaks Bantuan Sosial - Jebakan Dana Hibah Cair untuk UMKM"
            isi_teks = "Seorang pemilik warung kelontong SOHO menerima pesan WhatsApp dengan link bertuliskan: 'Pendaftaran Program Dana Bantuan Sosial Tunai UMKM Pemulihan Ekonomi Nasional Gelombang IV Tahap 2 sebesar Rp5.000.000. Kuota terbatas untuk 100 toko pertama. Klik link cek-penerima-bansos-umkm.online untuk pencairan dana instant.' Korban yang tergiur modal tambahan langsung mengklik link tersebut, mengisi data login rekening marketplace tokonya, and menyerahkan nomor OTP SMS-nya ke peretas."
            tips_teks = "Kementerian Sosial atau dinas terkait tidak pernah menyalurkan dana bantuan sosial tunai pendaftaran mandiri melalui link domain asing '.online' atau chat WhatsApp personal. Info resmi wajib diverifikasi lewat portal web kementerian kepala negara."
            soal_teks = "Toko Anda menerima link chat pendaftaran gratis dana hibah bansos UMKM Rp5 Juta menggunakan domain '.online'. Tindakan pertahanan Anda?"
            opsi_sidang = st.session_state.list_opsi_m10
            next_hal = 14  # Siap dilempar ke materi selanjutnya besok

                # ----------------- HALAMAN 14: MATERI 11 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 14:
            mid, nomor, judul = "m11", 11, "Materi 11: Investasi Bodong - Modus Grup Telegram/WA Tugas Like & Share Berbayar"
            isi_teks = "Seorang pelaku usaha katering dimasukkan secara otomatis oleh nomor asing ke dalam sebuah grup chat WhatsApp bernama 'Tugas Sampingan UMKM Sukses'. Di dalam grup tersebut, puluhan akun fiktif (bot/penipu) saling mengirimkan bukti transfer palsu and bersaksi telah menerima komisi harian hingga Rp2.000.000 hanya dengan menyelesaikan tugas mudah: memberikan *Like* and *Share* pada video produk tertentu. Pada 3 tugas pertama, korban diberikan bonus asli sebesar Rp50.000 untuk memancing kepercayaan. Namun pada tugas ke-4, korban diwajibkan melakukan *Deposit Top-Up Dana Modal* sebesar Rp5.000.000 dengan janji uang kembali Rp7.500.000 dalam 30 menit. Korban yang tergiur langsung mentransfer uang modal belanjanya, and detik itu juga admin grup memblokir nomor korban and membawa lari uangnya."
            tips_teks = "Modus kejahatan investasi siber komisi instan selalu menggunakan teknik psikologi psikologis umpan kecil di awal. Jika sebuah pekerjaan menawarkan keuntungan tidak masuk akal and meminta Anda mentransfer deposit uang terlebih dahulu, itu adalah 100% skema penipuan Ponzi."
            soal_teks = "Anda dimasukkan ke grup asing yang menjanjikan uang jutaan rupiah per hari hanya dengan memberi like video, tetapi Anda diwajibkan mentransfer uang deposit jaminan modal toko terlebih dahulu. Tindakan proteksi Anda?"
            opsi_sidang = st.session_state.list_opsi_m11
            next_hal = 15  # Lurus maju ke Halaman 15 (Materi 12)

        # ----------------- HALAMAN 15: MATERI 12 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 15:
            mid, nomor, judul = "m12", 12, "Materi 12: Phishing Saham - Jebakan File APK Pembagian Dividen Emiten Palsu"
            isi_teks = "Pak Khendy memiliki investasi saham kecil-kecilan untuk aset masa depan keluarganya. Suatu hari, sebuah pesan SMS masuk dari nomor biasa menggunakan nama samaran sekuritas ternama: *'Pemberitahuan Emiten: Selamat! Akun investasi Anda berhak menerima dana dividen tunai tambahan sebesar Rp3.500.000 dari keuntungan kuartal ini. Silakan unduh and verifikasi portofolio Anda melalui aplikasi resmi Berkas_Dividen_Saham.apk di bawah ini sebelum hangus.'* Karena gembira and tidak ingin kehilangan hak bonus keuntungannya, korban langsung menginstal aplikasi tersebut. Malware Trojan di dalamnya langsung menyadap token m-banking di HP and menguras isi portofolionya."
            tips_teks = "Pengumuman pembagian dividen saham resmi perusahaan selalu disiarkan lewat email terdaftar resmi sekuritas, menu keterbukaan informasi di aplikasi trading resmi, atau surat pos fisik dari Kustodian Sentral Efek Indonesia (KSEI). Tidak ada emiten saham yang membagikan dividen lewat file aplikasi APK nomor handphone pribadi."
            soal_teks = "Anda menerima SMS dari nomor handphone pribadi mengatasnamakan bursa saham, melampirkan file berkas 'Berkas_Dividen_Saham.apk' and meminta Anda segera memverifikasi data portofolio modal Anda. Tindakan paling aman?"
            opsi_sidang = st.session_state.list_opsi_m12
            next_hal = 16  # Gerbang jembatan menuju Halaman Rapor Akhir Batch 3 Akbar!

        st.markdown(f"### 📘 {judul}")
        st.write(isi_teks)
        st.info(f"💡 **Trik Lapangan:** {tips_teks}")
        st.markdown("---")
        st.subheader(f"✍️ UJIAN MANDIRI MATERI {nomor}")
        st.write(soal_teks)

        terkunci = mid in st.session_state.materi_selesai
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
            
            teks_lanjut = f"Materi Selanjutnya (Materi {nomor + 1}) ➡️" if nomor != 4 and nomor != 8 else "Buka Halaman Rapor Evaluasi Akhir 📊"
            if st.button(teks_lanjut, use_container_width=True):
                # UPDATE RECORD HALAMAN TERAKHIR KE DATABASE SEBELUM BERPINDAH
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET halaman_terakhir = ? WHERE email = ?", (next_hal, st.session_state.user_email))
                conn.commit()
                conn.close()
                
                st.session_state.halaman_sekarang = next_hal
                st.rerun()

    # --- HALAMAN 6: GERBANG RAPOR EVALUASI BATCH 1 (SYARAT MUTLAK SKOR 4/4) ---
    elif st.session_state.halaman_sekarang == 6:
        st.markdown("### 📊 Rapor Evaluasi: Pembatasan Batch 1 (Materi 1 - 4)")
        
        skor_b1 = sum([1 for m_id in ["m1", "m2", "m3", "m4"] if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]])
        salah_b1 = 4 - skor_b1
        
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT remidi_b1 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        # 👉 PERBAIKAN: Ekstrak nilai indeks 0 dari tuple database dengan aman
        total_remidi_b1 = data_remidi[0] if data_remidi else 0
        
        st.metric("Jumlah Upaya Percobaan Batch 1", f"{total_remidi_b1} Kali")
        st.markdown("---")

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
            st.success("👑 **STATUS BATCH 1: LULUS TOTAL (4/4)**\n\nGerbang kurikulum lanjutan Modul 1 (Kategori Dokumen APK Bahaya) resmi dibuka!")
            
            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE pengguna SET status_lulus_b1 = 1 WHERE email = ?", (st.session_state.user_email,))
            conn.commit()
            conn.close()
            
            if st.button("Maju ke Batch 2: Materi Lanjutan (Materi 5) 🔓🚀", type="primary", use_container_width=True):
                st.session_state.halaman_sekarang = 7
                st.rerun()
        else:
            st.error(f"🚨 **STATUS BATCH 1: WAJIB REMIDI ({skor_b1}/4 BENAR)**\n\nSelesaikan remedial kuis 100% benar untuk melanjutkan!")
            if st.button("🔄 Ulangi Ujian Batch 1 (Urutan Kalimat di-Shuffle Kembali 🎲)", type="primary", use_container_width=True):
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

    # --- HALAMAN 12: RAPOR AKHIR SEMENTARA BATCH 2 (MATERI 5 - 8 LULUS FINAL!) ---
            # 👉 KUNCI MATEMATIKA SINKRON: Mengizinkan hanya halaman kuis murni saja yang masuk ke mesin sensor tengah
    #elif (2 <= st.session_state.halaman_sekarang <= 5) or (7 <= st.session_state.halaman_sekarang <= 10) or (12 <= st.session_state.halaman_sekarang <= 15):
    elif st.session_state.halaman_sekarang == 11:
        st.markdown("### 📊 Rapor Akhir Evaluasi: Hasil Komulatif (Materi 1 - 8)")
        st.write("Selamat! Anda telah merampungkan 8 materi dasar. Berikut adalah analisis total ketahanan siber komulatif Anda:")
        
        skor_komulatif = 0
        for m_id in ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8"]:
            if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]:
                skor_komulatif += 1
        salah_komulatif = 8 - skor_komulatif

        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT remidi_b1, remidi_b2 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        
        # 👉 PERBAIKAN: Mengekstrak indeks tuple database 0 dan 1 secara aman untuk Batch 2
        total_remidi_b1 = data_remidi[0] if data_remidi else 0
        total_remidi_b2 = data_remidi[1] if data_remidi else 0

        col_m1, col_m2 = st.columns(2)
        with col_m1: st.metric("Percobaan Remidi Batch 1", f"{total_remidi_b1} Kali")
        with col_m2: st.metric("Percobaan Remidi Batch 2", f"{total_remidi_b2} Kali")
        st.markdown("---")

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
        if skor_komulatif == 8:
            st.success(f"👑 **STATUS EVALUASI: LULUS SEMPURNA (8/8 BENAR)**\n\nSelamat, Kelulusan Anda resmi tercatat di database!")
            
            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE pengguna SET status_lulus_b2 = 1, halaman_terakhir = 12 WHERE email = ?", (st.session_state.user_email,))
            conn.commit()
            conn.close()
            
            if st.button("Maju ke Batch 3: Materi Lanjutan (Materi 9) 🔓🚀", type="primary", use_container_width=True):
                st.session_state.halaman_sekarang = 12
                st.rerun()
        else:
            st.error(f"🚨 **STATUS EVALUASI: WAJIB REMIDI ({skor_komulatif}/8 BENAR)**\n\nSelesaikan remedial kuis Batch 2 sampai sempurna!")
            if st.button("🔄 Ulangi Ujian Khusus Batch 2 (Kalimat di-Shuffle Kembali 🎲)", type="primary", use_container_width=True):
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET remidi_b2 = remidi_b2 + 1 WHERE email = ?", (st.session_state.user_email,))
                conn.commit()
                conn.close()
                
                for mid in ["m5", "m6", "m7", "m8"]:
                    if mid in st.session_state.materi_selesai: st.session_state.materi_selesai.remove(mid)
                    if mid in st.session_state.jawaban_user: del st.session_state.jawaban_user[mid]
                    if mid in st.session_state.pilihan_text_save: del st.session_state.pilihan_text_save[mid]
                
                random.shuffle(st.session_state.list_opsi_m5)
                random.shuffle(st.session_state.list_opsi_m6)
                random.shuffle(st.session_state.list_opsi_m7)
                random.shuffle(st.session_state.list_opsi_m8)
                st.session_state.halaman_sekarang = 7  
                st.rerun()

    # ----------------- HALAMAN 16: RAPOR AKHIR BATCH 3 (MATERI 9 - 12 LULUS FINAL B3!) -----------------
    elif st.session_state.halaman_sekarang == 16:
        st.markdown("### 📊 Rapor Akhir Evaluasi: Hasil Komulatif (Materi 1 - 12)")
        st.write("Selamat! Anda telah merampungkan rumpun materi manipulasi hoaks informasi massa and penipuan investasi bodong finansial. Berikut analisis total ketahanan siber komulatif Anda:")
        
        # 1. HITUNG SKOR KOMULATIF NYATA (TOTAL DARI 12 MATERI YANG SUDAH DIBUKA)
        skor_komulatif = 0
        for m_id in ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12"]:
            if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]:
                skor_komulatif += 1
        salah_komulatif = 12 - skor_komulatif

        # Tarik data status kelulusan and remidi dari database SQLite
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        # Membuat kolom penampung remidi_b3 otomatis jika belum ada di database laptop Anda
        try: cursor.execute("ALTER TABLE pengguna ADD COLUMN remidi_b3 INTEGER DEFAULT 0"); conn.commit()
        except sqlite3.OperationalError: pass
        try: cursor.execute("ALTER TABLE pengguna ADD COLUMN status_lulus_b3 INTEGER DEFAULT 0"); conn.commit()
        except sqlite3.OperationalError: pass
        
        cursor.execute("SELECT remidi_b1, remidi_b2, remidi_b3 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        
        total_remidi_b1 = data_remidi[0] if data_remidi else 0
        total_remidi_b2 = data_remidi[1] if data_remidi else 0
        total_remidi_b3 = data_remidi[2] if data_remidi else 0

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1: st.metric("Remidi Batch 1", f"{total_remidi_b1} Kali")
        with col_m2: st.metric("Remidi Batch 2", f"{total_remidi_b2} Kali")
        with col_m3: st.metric("Remidi Batch 3", f"{total_remidi_b3} Kali")
        st.markdown("---")

        # 2. VISUALISASI SATU PIE CHART BESAR DI TENGAH (KONSISTEN SUPER BERSIH)
        col_tengah1, col_tengah2, col_tengah3 = st.columns([1, 2, 1])
        with col_tengah2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🎯 Grafik Akurasi Komulatif Kelas (Materi 1 - 12)</p>", unsafe_allow_html=True)
            fig_b3, ax_b3 = plt.subplots(figsize=(3, 3))
            ax_b3.pie([skor_komulatif, salah_komulatif], labels=[f"Aman ({skor_komulatif})", f"Celah ({salah_komulatif})"], colors=['#2ECC71', '#E74C3C'], autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax_b3.axis('equal')  
            fig_b3.patch.set_facecolor('#1E1E1E')
            ax_b3.set_facecolor('#1E1E1E')
            st.pyplot(fig_b3)

        st.markdown("---")
        
        # 3. LOGIKA KELULUSAN BATCH 3 MUTLAK
        # Pengguna wajib benar minimal pada materi Batch 3 (M9, M10, M11, M12) and total skor komulatif bernilai bagus
        skor_b3_murni = sum([1 for m_id in ["m9", "m10", "m11", "m12"] if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]])
        
        if skor_b3_murni == 4:
            st.success(f"👑 **STATUS EVALUASI BATCH 3: LULUS TOTAL (4/4 BENAR BATCH 3)**\n\nSelamat, {st.session_state.user_email}! Anda berhasil menjinakkan seluruh skenario manipulasi berita hoaks massal and jebakan skema Ponzi. Gerbang Materi Lanjutan resmi terbuka!")
            
            # Kunci kelulusan Batch 3 ke database
            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE pengguna SET status_lulus_b3 = 1, halaman_terakhir = 17 WHERE email = ?", (st.session_state.user_email,))
            conn.commit()
            conn.close()
            
            if st.button("Maju ke Batch 4: Kurikulum Proteksi Pamungkas (Materi 13) 🔓🚀", type="primary", use_container_width=True):
                st.session_state.halaman_sekarang = 17  # Pintu masuk menuju kurikulum Batch 4 besok
                st.rerun()
        else:
            st.error(f"🚨 **STATUS EVALUASI BATCH 3: WAJIB REMIDI ({skor_b3_murni}/4 BENAR PADA BATCH 3)**\n\nSistem mendeteksi psikologi emosi Anda masih rentan tergiur oleh keuntungan instan investasi bodong. Silakan ulangi ujian khusus modul ini!")
            
            if st.button("🔄 Ulangi Ujian Khusus Batch 3 (Kalimat di-Shuffle Kembali 🎲)", type="primary", use_container_width=True):
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET remidi_b3 = remidi_b3 + 1 WHERE email = ?", (st.session_state.user_email,))
                conn.commit()
                conn.close()
                
                # Reset memori kuis khusus Batch 3 saja (M9 sampai M12) agar Batch 1 and 2 tetap aman terkunci
                for mid in ["m9", "m10", "m11", "m12"]:
                    if mid in st.session_state.materi_selesai: st.session_state.materi_selesai.remove(mid)
                    if mid in st.session_state.jawaban_user: del st.session_state.jawaban_user[mid]
                    if mid in st.session_state.pilihan_text_save: del st.session_state.pilihan_text_save[mid]
                
                # Kocok ulang formsasi jawaban khusus Batch 3
                random.shuffle(st.session_state.list_opsi_m9)
                random.shuffle(st.session_state.list_opsi_m10)
                random.shuffle(st.session_state.list_opsi_m11)
                random.shuffle(st.session_state.list_opsi_m12)
                st.session_state.halaman_sekarang = 12  # Balik otomatis ke awal mula Batch 3 (Materi 9)
                st.rerun()
