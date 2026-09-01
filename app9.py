import streamlit as st
import sqlite3
import streamlit.components.v1 as components  # 👉 PASTIKAN BARIS INI ADA DI PALING ATAS FILE
import random
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO
from datetime import datetime

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.colors import HexColor, black, white
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics
    REPORTLAB_READY = True
except ImportError:
    REPORTLAB_READY = False
    canvas = None
    A4 = None
    HexColor = None
    black = None
    white = None
    TTFont = None
    pdfmetrics = None

# 1. Pengaturan Awal Tampilan Halaman Web
st.set_page_config(page_title="GardaDigital - Sistem Akun & Anti-Cheat", page_icon="🛡️", layout="centered")

# CSS tambahan agar aplikasi lebih ramah di browser smartphone
st.markdown(
    """
    <style>
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1.5rem !important;
        max-width: 1100px !important;
    }

    [data-testid="stAppViewContainer"] {
        overflow: visible !important;
    }

    section.main > div {
        padding-top: 0.4rem !important;
    }

    div[data-testid="stSidebar"] {
        min-width: 260px;
    }

    @media (max-width: 768px) {
        .block-container {
            padding-left: 0.7rem !important;
            padding-right: 0.7rem !important;
            padding-top: 0.8rem !important;
        }

        div[data-testid="stSidebar"] {
            min-width: 100% !important;
            max-width: 100% !important;
        }

        .stButton > button,
        .stDownloadButton > button,
        [data-testid="baseButton-secondary"] {
            width: 100% !important;
            min-height: 44px !important;
            white-space: normal !important;
        }

        .stTabs [role="tablist"] {
            overflow-x: auto;
            flex-wrap: nowrap;
            scrollbar-width: thin;
        }

        .stTabs [role="tab"] {
            min-width: 170px;
            white-space: nowrap;
        }

        .stRadio > div[role="radiogroup"] {
            gap: 0.5rem;
        }

        .stRadio > div[role="radiogroup"] > label {
            padding: 0.55rem 0.75rem;
            border-radius: 0.6rem;
            border: 1px solid rgba(49, 51, 63, 0.15);
            margin-bottom: 0.4rem;
        }

        .stDataFrame, .stTable, .stPlotlyChart, .stAltairChart, .stECharts, .stVegaLiteChart {
            overflow-x: auto;
        }

        h1, h2, h3, h4, h5, h6 {
            word-wrap: break-word;
            overflow-wrap: break-word;
            line-height: 1.2;
            white-space: normal;
            margin-top: 0.25rem !important;
            margin-bottom: 0.75rem !important;
        }

        p, li, div, span {
            word-wrap: break-word;
            overflow-wrap: break-word;
            line-height: 1.6;
            margin-bottom: 0.6rem;
        }

        .stImage > img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 0 auto;
            border-radius: 10px;
        }
    }

    .premium-box {
        background: linear-gradient(180deg, rgba(255,255,255,0.96), rgba(245,247,250,0.96));
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 14px;
        padding: 1rem 1rem 0.5rem 1rem;
        margin: 0.7rem 0 1rem 0;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.06);
    }

    .premium-box h4 {
        margin: 0 0 0.55rem 0;
        color: #0f172a;
        font-size: 1.05rem;
    }

    .premium-box ul {
        margin: 0.35rem 0 0 1.1rem;
        padding: 0;
        color: #334155;
    }

    .premium-box li {
        margin-bottom: 0.5rem;
        line-height: 1.55;
    }

    .batch-chip {
        display: inline-block;
        background: #f1f5f9;
        color: #0f172a;
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 999px;
        padding: 0.35rem 0.7rem;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


import streamlit as st
import streamlit.components.v1 as components  # 👉 PASTIKAN BARIS INI ADA DI PALING ATAS FILE

def render_brand_header(width=220, subtitle_color="#3A3A3A"):
    # 👉 1. KUNCI RAHASIA: Menaruh wadah kosong di puncak tertinggi halaman untuk menarik fokus scroll ke atas
    puncak_halaman = st.empty()
    
    # 2. HANCURKAN BATAS ATAS STREAMLIT (CSS TETAP KOKOH DAN DIALOKASIKAN AMAN)
    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem !important;
                padding-bottom: 0rem !important;
            }
            [data-testid="stSidebarUserContent"] {
                padding-top: 2rem !important;
            }
            header {
                visibility: hidden !important;
                height: 0px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 3. AREA RENDERING LOGO KEBANGGAAN ANDA
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode("utf-8")
        st.markdown(
            f"""
            <div style='display: flex; justify-content: center; align-items: center; text-align: center; margin: 0 auto;'>
                <div style='display: inline-block; text-align: center;'>
                    <img src='data:image/png;base64,{encoded}' alt='GardaDigital Logo' style='width: {width}px; max-width: 100%; height: auto; display: inline-block; margin-top: 15px; margin-bottom: 5px;' />
                    <p style='text-align: center; color: {subtitle_color}; font-size: 15px; font-weight: 500; margin-top: 10px; margin-bottom: 12px; line-height: 1.4;'>Aplikasi Pelatihan Keamanan Digital untuk<br>UMKM, SOHO, & Masyarakat Umum</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown("<h1 style='text-align: center; padding-top: 15px;'>🛡️ GardaDigital</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #3A3A3A; font-size: 15px; font-weight: 500; margin-top: 10px; margin-bottom: 12px; line-height: 1.4;'>Aplikasi Pelatihan Keamanan Digital untuk<br>UMKM, SOHO, & Masyarakat Umum</p>", unsafe_allow_html=True)

def buat_sertifikat_modul1_pdf(nama_lengkap: str, instansi: str, tanggal_lulus: str):
    if not REPORTLAB_READY:
        return None

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setTitle("Sertifikat GardaDigital Modul 1")
    c.setAuthor("GardaDigital")

    # 1. LATAR BELAKANG PUTIH BERSIH ELEGAN
    c.setFillColor(HexColor("#F8FAFC"))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # 2. BINGKAI GANDA MINIMALIS (BIRU NAVY & ABU-ABU PERAK)
    # Bingkai Luar: Biru Navy Kokoh
    c.setStrokeColor(HexColor("#1E3A5F")) # Navy Blue
    c.setLineWidth(4)
    c.rect(36, 36, width - 72, height - 72, fill=0, stroke=1)

    # Bingkai Dalam: Abu-abu Perak Tipis
    c.setStrokeColor(HexColor("#CBD5E1")) # Silver Grey
    c.setLineWidth(1.5)
    c.rect(48, 48, width - 96, height - 96, fill=0, stroke=1)

       # 3. LOGO GARDA DIGITAL UTAMA SAKTI (Biarkan di posisi ideal ini)
    logo_path = "logo.png" if os.path.exists("logo.png") else None
    if logo_path:
        logo_width = 80
        logo_height = 80
        c.drawImage(logo_path, (width - logo_width) / 2, 675, width=logo_width, height=logo_height, mask='auto')

    # 4. 👉 PERBAIKAN TOTAL KOORDINAT TEKS JURUS TURUN BAWAH
    c.setFillColor(HexColor("#1E3A5F"))
    c.setFont("Helvetica-Bold", 26)
    # 🔄 Diubah dari 655 menjadi 625 agar tidak tertabrak logo
    c.drawCentredString(width / 2, 625, "SERTIFIKAT KELULUSAN")

    c.setFont("Helvetica", 14)
    c.setFillColor(HexColor("#6B7280"))
    # 🔄 Diubah dari 625 menjadi 595 agar jaraknya tetap proporsional
    c.drawCentredString(width / 2, 595, "Sistem Pelatihan Kesadaran Siber GardaDigital")

    # Garis Pembatas Horisontal
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.setLineWidth(1.2)
    # 🔄 Diubah dari 605 menjadi 575 agar sejajar di bawah teks subjudul
    c.line(160, 575, width - 160, 575)

        # 5. DATA IDENTITAS INTEGRASI PROFIL (TUMPUKAN MATERI TENGAH)
    c.setFillColor(HexColor("#475569"))
    c.setFont("Helvetica-Oblique", 13)
    c.drawCentredString(width / 2, 530, "Sertifikat ini secara resmi diberikan kepada:")

    # Nama Pengguna (Warna Navy Gelap)
    c.setFillColor(HexColor("#0F172A"))
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, 485, nama_lengkap.upper())

    # 👉 PERBAIKAN KOORDINAT JURUS GESER TURUN BAWAH (ANTI-MEPET)
    c.setFillColor(HexColor("#475569"))
    c.setFont("Helvetica", 14)
    # 🔄 Diubah dari 465 menjadi 435 agar memberi jarak napas di bawah nama
    c.drawCentredString(width / 2, 435, "Telah dinyatakan Lulus and Kompeten pada kurikulum:")
    
    c.setFillColor(HexColor("#1E3A5F"))
    c.setFont("Helvetica-Bold", 15)
    # 🔄 Diubah dari 440 menjadi 410 agar mengikuti penurunan teks di atasnya
    c.drawCentredString(width / 2, 410, "Modul 1: Social Engineering & Pertahanan Siber Dasar")

    c.setFillColor(HexColor("#6B7280"))
    c.setFont("Helvetica", 13)
    # 🔄 Diubah dari 405 menjadi 375 agar nama instansi user terlihat rapi and lapang
    c.drawCentredString(width / 2, 375, f"Asal Mitra / Instansi Toko: {instansi}")

    # 🔄 Diubah dari 350 menjadi 320 agar tulisan Klasifikasi Dasar bergeser proporsional ke bawah
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(HexColor("#94A3B8"))
    c.drawCentredString(width / 2, 320, "KLASIFIKASI: TINGKAT DASAR (BASIC SECURITY AWARENESS CERTIFICATION)")

        # 6. 🏆 SUNTIKAN FINAL SAKTI: Menggeser turun and memperkecil tanda tangan asli Anda
    try:
        # 👉 PERBAIKAN: Koordinat Y diturunkan dari 172 menjadi 166 agar pas menempel di atas garis
        # 👉 PERBAIKAN: Lebar dikecilkan dari 130 ke 95, tinggi disesuaikan dari 45 ke 38 agar proposional
        c.drawImage("images/ttd.png", width - 195, 166, width=95, height=38, mask='auto')
    except:
        try:
            c.drawImage("ttd.png", width - 195, 166, width=95, height=38, mask='auto')
        except:
            pass

    # Garis tanda tangan hitam formal (Biarkan tetap utuh and lurus)
    c.setStrokeColor(HexColor("#1E3A5F"))
    c.setLineWidth(1)
    c.line(width - 240, 165, width - 80, 165)
    
    # Informasi Nama Terang di bawah garis
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(HexColor("#1E3A5F"))
    c.drawRightString(width - 105, 145, "KHENDY REDYA")
    
    c.setFont("Helvetica", 10)
    c.setFillColor(HexColor("#6B7280"))
    c.drawRightString(width - 108, 128, "Founder GardaDigital")

        # 7. 👑 PERBAIKAN: MENGGESER LINGKARAN & STEMPEL LOGO KE SEBELAH KANAN LUAR (ANTI-BERTUMPUKAN)
    # 👉 PERBAIKAN: Sumbu X lingkaran digeser ke kanan dari (width - 150) menjadi (width - 110)
    c.setStrokeColor(HexColor("#CBD5E1"))
    c.setLineWidth(1.5)
    c.circle(width - 110, 180, 26) # Jari-jari lingkaran sedikit dirapatkan menjadi 26
    
    try:
        c.saveState()
        c.setFont("Helvetica-Bold", 7)
        c.setFillAlpha(0.3) # Efek transparan abu-abu tipis 30% tetap dikunci aman
        
        # 👉 PERBAIKAN: Sumbu X gambar ikut digeser ke kanan dari (width - 171) menjadi (width - 131)
        # Ukuran logo sedikit dirapatkan (lebar 40, tinggi 32) agar presisi di dalam rumah lingkaran baru
        c.drawImage("logo.png", width - 131, 164, width=40, height=32, mask='auto')
        
        c.restoreState()
    except:
        try:
            c.saveState()
            c.setFillAlpha(0.3)
            c.drawImage("logo.PNG", width - 131, 164, width=40, height=32, mask='auto')
            c.restoreState()
        except:
            c.setFont("Helvetica-Bold", 7)
            c.setFillColor(HexColor("#CBD5E1"))
            c.drawCentredString(width - 110, 183, "GARDA")
            c.drawCentredString(width - 110, 174, "DIGITAL")


    # 8. NOMOR REGISTRASI DATA PENGGUNA (ANTI-PALSU POJOK KIRI BAWAH)
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Courier", 9)
    c.drawString(75, 155, f"No. Registrasi: GD-M1-BASIC-{tanggal_lulus.replace(' ', '')}")
    c.drawString(75, 140, "Diverifikasi Otomatis Melalui Sistem Database Garda Digital")

    # 9. FOOTER KECIL PENUTUP
    c.setFillColor(HexColor("#94A3B8"))
    c.setFont("Helvetica-Oblique", 9)
    c.drawCentredString(width / 2, 88, "SaaS Perlindungan Aset Digital Bisnis & Personal Awareness")

    c.save()
    return buffer.getvalue()


# Reset posisi scroll setiap kali halaman dirender agar materi selalu terbuka dari atas.
def reset_scroll_ke_atas():
    # 👉 KUNCI SEMBUH MUTLAK: Membuat elemen jangkar tidak terlihat tepat di koordinat 0 puncak halaman
    st.markdown("<div id='puncak-garda-utama'></div>", unsafe_allow_html=True)
    
    # Menyuntikkan tautan otomatis tersembunyi yang memaksa browser melompat ke ID di atas saat elemen dimuat
    st.markdown(
        """
        <a id="klik-puncak-otomatis" href="#puncak-garda-utama" target="_self" style="display:none;">Scroll</a>
        <script>
            // Menembak paksa klik simulasi pada link jangkar di atas demi mendobrak fokus otomatis kontainer
            setTimeout(function(){
                const linkJangkar = window.parent.document.getElementById("klik-puncak-otomatis") || document.getElementById("klik-puncak-otomatis");
                if(linkJangkar) { linkJangkar.click(); }
                // Backup commands jika browser mobile sangat ketat
                window.parent.document.querySelector(".main").scrollTo(0,0);
            }, 50);
        </script>
        """,
        unsafe_allow_html=True
    )

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
    "m12": "Mengabaikan instruksi SMS tersebut dan memblokir nomornya, karena pengumuman resmi pembagian dividen atau urusan saham emiten selalu dikirimkan lewat surat fisik resmi KSEI atau menu keterbukaan informasi aplikasi sekuritas resmi.",
    "m13": "Menolak memberikan kode 6 angka tersebut kepada siapa pun, karena itu adalah kode verifikasi OTP untuk mengambil alih akun WhatsApp Anda.",
    "m14": "Menolak mengunduh atau menginstal file tersebut, karena kurir resmi tidak pernah mengirimkan resi atau foto paket dalam format aplikasi .APK.",
    "m15": "Mengecek mutasi saldo masuk secara mandiri melalui aplikasi m-banking resmi toko, bukan hanya percaya pada gambar struk fisik yang dikirim pembeli.",
    "m16": "Segera mengaktifkan fitur Verifikasi Dua Langkah (Two-Factor Authentication) di menu pengaturan keamanan akun WhatsApp toko Anda.",
    "m17": "Jangan buka attachment atau klik link dari email mencurigakan, langsung hubungi supplier/bank/marketplace melalui nomor resmi untuk konfirmasi, and laporkan email phishing ke tim keamanan.",
    "m18": "Menggugat klaim dan meminta bukti identitas (foto KTP), tidak langsung mengirim dana atau data sensitif, and cek nomor telepon melalui website resmi sebelum memberikan informasi.",
    "m19": "Hindari berbagi informasi bisnis di media sosial publik, verifikasi akun seller sebelum berkomunikasi, and laporkan akun imposter ke tim support platform marketplace.",
    "m20": "Lakukan edukasi rutin untuk tim UMKM tentang taktik social engineering, buat checklist verifikasi sender/caller, and bangun budaya untuk selalu skeptis terhadap permintaan data/uang urgent."


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
    st.session_state.list_opsi_m1 = [
        "Karena penipu biasanya menargetkan titik paling lemah dalam keputusan manusia, bukan hanya kekuatan sistem keamanan bank.",
        "Manusia memiliki celah emosi (panik/lengah) yang jauh lebih mudah dimanipulasi daripada menembus pertahanan kode keamanan digital bank.",
        "Karena sistem keamanan mobile banking di Indonesia memang tidak memiliki pengamanan sama sekali.",
        "Karena kalau korban tidak panik, penipu tidak akan bisa mengakses rekening atau data apapun."
    ]
    random.shuffle(st.session_state.list_opsi_m1)

if "list_opsi_m2" not in st.session_state:
    st.session_state.list_opsi_m2 = [
        "Mengabaikan SMS tersebut, lalu mengecek saldo secara mandiri lewat aplikasi Mobile Banking resmi atau datang ke mesin ATM terdekat.",
        "Segera membalas SMS dengan format yang sama agar penipu merasa dihormati dan tidak menghubungi lagi.",
        "Menekan tombol konfirmasi di SMS tersebut karena kemungkinan itu adalah komunikasi resmi dari bank.",
        "Mengirimkan kode OTP ke nomor lain agar bank bisa memverifikasi bahwa rekening Anda masih aktif."
    ]
    random.shuffle(st.session_state.list_opsi_m2)

if "list_opsi_m3" not in st.session_state:
    st.session_state.list_opsi_m3 = [
        "Memastikan lambang centang hijau resmi berada di sebelah kanan nama profil akun, bukan di dalam gambar foto profil bulatan.",
        "Melihat apakah foto profil akun tersebut menggunakan warna biru yang modern agar terlihat lebih meyakinkan.",
        "Memastikan nama kontak dibuat mirip dengan nama asli agar terlihat resmi di mata korban.",
        "Mengecek apakah nomor WhatsApp tersebut berasal dari wilayah yang sama dengan lokasi usaha Anda."
    ]
    random.shuffle(st.session_state.list_opsi_m3)

if "list_opsi_m4" not in st.session_state:
    st.session_state.list_opsi_m4 = [
        "Mematikan telepon, langsung menghubungi nomor HP anak Anda secara mandiri, dan menyadari bahwa polisi asli tidak pernah meminta uang damai atau menyuruh warga berutang di Paylater.",
        "Meminta penipu mengirimkan foto identitas resmi supaya Anda yakin si pelaku benar-benar polisi.",
        "Membayar denda secara tunai terlebih dahulu agar masalah bisa selesai tanpa menimbulkan konflik lebih lanjut.",
        "Mengikuti arahan pelaku karena mereka biasanya datang dengan alasan yang sangat meyakinkan."
    ]
    random.shuffle(st.session_state.list_opsi_m4)

if "list_opsi_m5" not in st.session_state:
    st.session_state.list_opsi_m5 = [
        "Menolak menginstal file tersebut, langsung menghapus pesan, dan memeriksa status tilang secara mandiri melalui situs resmi ETLE Korlantas Polri menggunakan nomor pelat kendaraan.",
        "Menginstal file APK tersebut karena biasanya aplikasi pembuktian kejahatan selalu disebarkan lewat WhatsApp.",
        "Meneruskan file tersebut ke teman agar mereka ikut mengonfirmasi apakah ini benar-benar valid atau tidak.",
        "Membalas pesan lalu menyetujui seluruh syarat agar proses tilang bisa segera diselesaikan."
    ]
    random.shuffle(st.session_state.list_opsi_m5)

if "list_opsi_m6" not in st.session_state:
    st.session_state.list_opsi_m6 = [
        "Menghapus pesan tersebut dan mengabaikannya, karena instansi pajak resmi tidak pernah mengirimkan dokumen penagihan denda atau detail pajak dalam format aplikasi APK lewat WhatsApp pribadi.",
        "Mendownload file APK tersebut agar dapat memastikan apakah ada kesalahan pengenaan denda pajak terhadap usaha Anda.",
        "Membalas nomor pengirim untuk meminta data NPWP dan KTP agar pihak pajak bisa menghapus tunggakan secara cepat.",
        "Menghubungi nomor yang mengirim pesan lalu menyetujui semua langkah karena ini pasti berasal dari kantor pajak."
    ]
    random.shuffle(st.session_state.list_opsi_m6)

if "list_opsi_m7" not in st.session_state:
    st.session_state.list_opsi_m7 = [
        "Mengabaikan pesan WhatsApp tersebut dan memblokir nomornya, karena surat panggilan sidang resmi selalu dikirim melalui surat fisik pos tercatat ke alamat rumah.",
        "Menginstal aplikasinya karena dokumen resmi biasanya dibagikan dalam bentuk APK untuk mempermudah pengajuan.",
        "Membalasnya dan menanyakan nomor rekening agar bisa menutup perkara secepatnya agar nama tidak tercemar.",
        "Datang ke kantor polisi dengan membawa file APK agar sidang bisa dipercepat tanpa administrasi formal."
    ]
    random.shuffle(st.session_state.list_opsi_m7)

if "list_opsi_m8" not in st.session_state:
    st.session_state.list_opsi_m8 = [
        "Keluar dari chat WhatsApp tersebut, lalu membuka aplikasi atau website resmi Seller Center marketplace secara mandiri untuk mengecek status toko yang sebenarnya.",
        "Memberikan kode OTP karena admin marketplace memang sering meminta verifikasi agar akun tidak diblokir.",
        "Menyebarkan laporan penutupan akun ke pelanggan agar mereka tidak membatalkan pesanan toko.",
        "Langsung menginstal file yang dikirim agar toko bisa dibuka kembali secepatnya."
    ]
    random.shuffle(st.session_state.list_opsi_m8)

if "list_opsi_m9" not in st.session_state:
    st.session_state.list_opsi_m9 = [
        "Mengabaikan pesan hoaks tersebut, tidak ikut menyebarkannya, dan mengecek kebenaran informasi melalui situs resmi Bank Indonesia atau portal berita nasional yang terpercaya.",
        "Segera membagikan pesan itu ke grup usaha agar semua rekan tahu harus waspada sebelum uang ditarik bank.",
        "Langsung mengirimkan uang ke rekening yang disebutkan agar aman dari pemblokiran akun.",
        "Menyimpan pesan itu di folder favorit lalu mengecek lagi nanti bila sudah ramai dibicarakan."
    ]
    random.shuffle(st.session_state.list_opsi_m9)

if "list_opsi_m10" not in st.session_state:
    st.session_state.list_opsi_m10 = [
        "Menghapus pesan tersebut, tidak mengklik tautan apa pun, dan memverifikasi info bantuan sosial secara mandiri melalui situs resmi Cek Bansos Kemensos RI atau dinas sosial setempat.",
        "Langsung mengisi formulir yang dikirim agar tidak ketinggalan bantuan yang bisa memperlancar usaha.",
        "Mentransfer biaya administrasi dulu agar proses pencairan bantuan bisa dilakukan tanpa hambatan.",
        "Memberi tahu teman dekat untuk ikut mengisi soal yang sama agar semua bisa cepat mendapat dana."
    ]
    random.shuffle(st.session_state.list_opsi_m10)

if "list_opsi_m11" not in st.session_state:
    st.session_state.list_opsi_m11 = [
        "Segera keluar dari grup tersebut, mengabaikan tawaran keuntungan yang tidak masuk akal, dan tidak mentransfer uang sepeser pun karena itu adalah modus penipuan investasi skema Ponzi.",
        "Menyetor modal awal untuk memastikan apakah tawaran itu benar-benar bisa menghasilkan cuan cepat.",
        "Mengajak rekan kerja untuk ikut join karena peluangnya sangat bagus jika dikerjakan bersama-sama.",
        "Menyetujui semua instruksi karena biasanya promosi seperti itu memang selalu benar."
    ]
    random.shuffle(st.session_state.list_opsi_m11)

if "list_opsi_m12" not in st.session_state:
    st.session_state.list_opsi_m12 = [
        "Mengabaikan instruksi SMS tersebut dan memblokir nomornya, karena pengumuman resmi pembagian dividen atau urusan saham emiten selalu dikirimkan lewat surat fisik resmi KSEI atau menu keterbukaan informasi aplikasi sekuritas resmi.",
        "Membalas SMS dan memberikan data rekening karena klaim dividen tidak pernah meminta verifikasi tambahan.",
        "Mengunduh file yang dikirim karena pembagian aset biasanya membutuhkan aplikasi khusus yang dipasang dulu.",
        "Menyetorkan uang jaminan agar proses klaim bisa diproses lebih cepat tanpa menunggu surat resmi."
    ]
    random.shuffle(st.session_state.list_opsi_m12)

if "list_opsi_m13" not in st.session_state:
    st.session_state.list_opsi_m13 = [
        "Menolak memberikan kode 6 angka tersebut kepada siapa pun, karena itu adalah kode verifikasi OTP untuk mengambil alih akun WhatsApp Anda.",
        "Memberikan kode itu agar admin bisa memastikan bahwa nomor Anda masih aktif dan aman.",
        "Mengirim tangkapan layar kode itu ke teman agar mereka membantu mengecek apakah ini benar-benar aman.",
        "Memasukkan kode itu ke tautan yang dikirim agar proses pemulihan hadiah bisa diselesaikan."
    ]
    random.shuffle(st.session_state.list_opsi_m13)

if "list_opsi_m14" not in st.session_state:
    st.session_state.list_opsi_m14 = [
        "Menolak mengunduh atau menginstal file tersebut, karena kurir resmi tidak pernah mengirimkan resi atau foto paket dalam format aplikasi .APK.",
        "Membuka file APK itu karena semua bukti pengiriman sering dikirim dalam format aplikasi agar lebih praktis.",
        "Menyerahkan file tersebut ke pembeli agar mereka bisa menilai apakah paketnya sudah diterima atau belum.",
        "Menginstal aplikasi itu di laptop kantor agar semua proses operasional bisa berjalan tanpa gangguan."
    ]
    random.shuffle(st.session_state.list_opsi_m14)

if "list_opsi_m15" not in st.session_state:
    st.session_state.list_opsi_m15 = [
        "Mengecek mutasi saldo masuk secara mandiri melalui aplikasi m-banking resmi toko, bukan hanya percaya pada gambar struk fisik yang dikirim pembeli.",
        "Langsung mengirimkan pesanan karena pembeli sudah mengirimkan bukti transfer yang tampak resmi.",
        "Meminta foto KTP pembeli sebagai syarat validasi sebelum kirim barang agar lebih aman.",
        "Menghubungi layanan pelanggan bank untuk memastikan bahwa transfer masuk itu memang valid dan bukan data palsu."
    ]
    random.shuffle(st.session_state.list_opsi_m15)

if "list_opsi_m16" not in st.session_state:
    st.session_state.list_opsi_m16 = [
        "Segera mengaktifkan fitur Verifikasi Dua Langkah (Two-Factor Authentication) di menu pengaturan keamanan akun WhatsApp toko Anda.",
        "Mengubah password setiap minggu agar akun selalu terjaga dari serangan otomatis.",
        "Menghapus seluruh riwayat chat supaya hacker tidak bisa membaca percakapan lama Anda.",
        "Membeli handphone baru untuk admin agar semua aktivitas social engineering tidak bisa menargetkan akun lama."
    ]
    random.shuffle(st.session_state.list_opsi_m16)

if "list_opsi_m17" not in st.session_state:
    st.session_state.list_opsi_m17 = [
        "Jangan buka attachment atau klik link dari email mencurigakan, langsung hubungi supplier/bank/marketplace melalui nomor resmi untuk konfirmasi, dan laporkan email phishing ke tim keamanan.",
        "Membuka attachment karena email yang tampak sangat profesional biasanya aman dan tidak perlu diverifikasi ulang.",
        "Meneruskan email itu ke seluruh staf agar keputusan bersama bisa dibuat oleh tim yang lebih banyak.",
        "Mengabaikan email tersebut karena email phishing pasti selalu berbahasa Inggris dan tidak relevan."
    ]
    random.shuffle(st.session_state.list_opsi_m17)

if "list_opsi_m18" not in st.session_state:
    st.session_state.list_opsi_m18 = [
        "Menggugat klaim dan meminta bukti identitas (foto KTP), tidak langsung mengirim dana atau data sensitif, dan cek nomor telepon melalui website resmi sebelum memberikan informasi.",
        "Menyerahkan data pribadi karena penelepon jelas-jelas mengaku dari bank dan terdengar berwibawa.",
        "Langsung transfer uang karena pelanggan yang berasal dari bank biasanya tidak akan meminta transaksi palsu.",
        "Memberi nomor rekening agar pengecekan bisa langsung dilakukan tanpa perlu konfirmasi tambahan."
    ]
    random.shuffle(st.session_state.list_opsi_m18)

if "list_opsi_m19" not in st.session_state:
    st.session_state.list_opsi_m19 = [
        "Hindari berbagi informasi bisnis di media sosial publik, verifikasi akun seller sebelum berkomunikasi, dan laporkan akun imposter ke tim support platform marketplace.",
        "Langsung melakukan transfer ke akun pembeli yang terlihat memiliki verifikasi dengan banyak pengikut.",
        "Membagikan rekening dan nomor HP ke bio Instagram agar pembeli bisa cepat menghubungi tanpa proses verifikasi.",
        "Menganggap akun dengan tampilan profesional selalu aman karena sangat sulit dipalsukan."
    ]
    random.shuffle(st.session_state.list_opsi_m19)

if "list_opsi_m20" not in st.session_state:
    st.session_state.list_opsi_m20 = [
        "Lakukan edukasi rutin untuk tim UMKM tentang taktik social engineering, buat checklist verifikasi sender/caller, dan bangun budaya untuk selalu skeptis terhadap permintaan data/uang urgent.",
        "Menganggap social engineering tidak akan pernah terjadi pada bisnis kecil karena skala usaha terlalu kecil untuk menjadi target.",
        "Hanya pelatihan keamanan untuk pimpinan agar karyawan tidak perlu diajarkan hal yang sama.",
        "Berfokus pada password kuat saja tanpa membangun kebiasaan verifikasi dan edukasi rutin."
    ]
    random.shuffle(st.session_state.list_opsi_m20)


# =========================================================================
# 🧭 SIDEBAR NAVIGASI TERPADU (WHITE LABEL + RAPOR GLOBAL PINTAR)
# =========================================================================
if os.path.exists("logo.png"):
    col_logo_sidebar_l, col_logo_sidebar_c, col_logo_sidebar_r = st.sidebar.columns([1, 2, 1])
    with col_logo_sidebar_c:
        st.image("logo.png", width=68)
else:
    st.sidebar.markdown("<h2 style='text-align: center; margin-top: 0px;'>🛡️</h2>", unsafe_allow_html=True)

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

        st.session_state.halaman_sekarang = 0
        st.session_state.jawaban_user = {}
        st.session_state.materi_selesai = set()
        st.session_state.pilihan_text_save = {}
        st.session_state.intip_rapor_global = False

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
        random.shuffle(st.session_state.list_opsi_m13)
        random.shuffle(st.session_state.list_opsi_m14)
        random.shuffle(st.session_state.list_opsi_m15)
        random.shuffle(st.session_state.list_opsi_m16)

        st.success("🔄 Memori Ujian Berhasil Direset! Akun Anda kembali ke status awal.")
        st.rerun()

    if st.sidebar.button("✅ Simulasi Lulus & Buka Sertifikat", use_container_width=True, type="primary"):
        st.session_state.jawaban_user = {m: KUNCI_MATERI[m] for m in KUNCI_MATERI}
        st.session_state.materi_selesai = set(KUNCI_MATERI.keys())
        st.session_state.halaman_sekarang = 26
        st.session_state.intip_rapor_global = False
        st.rerun()

else:
    st.sidebar.write("🔒 Status: Silakan Masuk")
st.sidebar.markdown("---")

# =========================================================================
# 🏛️ INTERFACE UTAMA: GERBANG AUTH VS JALUR BELAJAR
# =========================================================================

# 👉 BARU: INTERFAS HALAMAN RAPOR GLOBAL JIKA TOMBOL SIDEBAR DIKLIK
if st.session_state.login_sukses and st.session_state.intip_rapor_global:
    st.markdown("### 📊 Rapor Global")
    
    total_materi_selesai = len(st.session_state.materi_selesai)
    total_materi_sisa = 20 - total_materi_selesai
    
    st.markdown(f"#### Progress Kelengkapan Kelas: **{total_materi_selesai} dari 20 Materi Selesai**")
    st.progress(total_materi_selesai / 20)
    
    col_g1, col_g2, col_g3 = st.columns([1, 2, 1])
    with col_g2:
        fig_g, ax_g = plt.subplots(figsize=(3, 3))
        ax_g.pie([total_materi_selesai, total_materi_sisa], labels=["Selesai", "Sisa Materi"], colors=['#2ECC71', '#555555'], autopct='%1.0f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
        ax_g.axis('equal')
        fig_g.patch.set_alpha(0)
        ax_g.set_facecolor('none')
        st.pyplot(fig_g)
        
    st.markdown("---")
    if st.button("⬅️ Kembali Melanjutkan Pembelajaran Materi", type="primary", use_container_width=True):
        st.session_state.intip_rapor_global = False
        st.rerun()
    st.stop()

# ----------------- KONDISI A: PENGGUNA BELUM LOGIN -----------------
if not st.session_state.login_sukses:
    render_brand_header(width=220, subtitle_color="#3A3A3A")
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
    reset_scroll_ke_atas()
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
            
        render_brand_header(width=220, subtitle_color="#2F2F2F")
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
        reset_scroll_ke_atas()
        st.markdown("## 🧠 Apa itu Social Engineering? (Penjelasan untuk Awam)")
        st.markdown("---")
        st.write("Bayangkan Anda memiliki rumah dengan gembok yang kuat dan kamera pengawas di setiap sudut. Rumah itu adalah sistem perbankan, toko online, atau akun digital Anda. Teknologi yang melindungi rumah itu—password, OTP, PIN, dan verifikasi keamanan—adalah lapisan pengaman yang seharusnya menjaga aset Anda.")
        st.write("Namun, penipu tidak selalu mencoba merusak pagar atau memecahkan kunci. Mereka sering memilih cara yang lebih licik: berpura-pura menjadi kurir, petugas bank, polisi, atau admin marketplace. Mereka datang dengan alasan yang menekan, membuat Anda panik, atau membuat Anda merasa harus cepat bertindak.")
        st.write("Misalnya, seseorang datang dengan alasan darurat lalu berkata, *'Permisi, ada paket penting yang harus segera masuk ke rumah. Tolong beri saya akses sebentar.'* Saat Anda merasa kasihan atau tergesa-gesa, Anda menyerahkan kunci atau akses yang sebenarnya sangat berharga. Dalam dunia digital, kunci itu bisa berarti PIN, kode OTP, password, atau data sensitif yang bisa membuka semua akun Anda.")
        st.write("Pola yang sama terjadi dalam dunia maya. Penipu tidak perlu memecahkan sistem keamanan Anda secara teknis. Mereka cukup memanfaatkan emosi: panik, rasa takut, keserakahan, atau keinginan untuk cepat selesai. Mereka lalu mendorong korban mengambil keputusan yang justru membuka celah sendiri, seperti mengirim kode OTP, mengklik tautan palsu, atau membagikan password.")
        st.write("Untuk melihat bagaimana ini bekerja, bayangkan seorang pemilik toko menerima chat WhatsApp dari nomor yang tampak seperti layanan resmi. Isi pesannya menyebutkan akun tokonya akan dibekukan dalam 10 menit jika tidak segera melakukan verifikasi. Di saat itulah rasa panik muncul. Korban yang tidak tenang lalu membuka link yang dikirim, memasukkan username, password, dan kode OTP ke halaman tiruan. Dalam hitungan menit, akun toko miliknya bisa dibajak dan saldo bisa habis.")
        st.write("Contoh itu bukan sekadar teori. Ini adalah pola yang terjadi berulang kali di masyarakat: penipu bukan hanya menyerang perangkat, tetapi menyerang keadaan mental korban. Mereka mengandalkan rasa takut, keinginan cepat, dan kepercayaan yang belum diperiksa. Karena itu, penguasaan terhadap emosi sendiri menjadi bagian penting dari keamanan digital.")
        st.success("💡 **Itulah Social Engineering.** Bukan sekadar soal teknologi, tetapi soal bagaimana manusia bisa dipengaruhi, ditipu, dan dibujuk untuk menyerahkan akses atau data penting tanpa sadar. Ancaman terbesar sering kali bukan pada sistem itu sendiri, melainkan pada keputusan yang diambil saat seseorang sedang terburu-buru, ketakutan, atau tergoda.")
        st.write("Karena itu, keamanan digital bukan hanya soal perangkat, tetapi juga soal cara berpikir. Ketika ada orang yang meminta data, uang, atau akses dengan alasan mendesak, langkah paling aman adalah berhenti sejenak, mengecek kebenaran, dan tidak langsung percaya. Yang paling sering diretas bukanlah server, melainkan manusia yang sedang tidak tenang.")

        st.markdown("### 🔍 Gambaran Besar Modul 1")
        st.write("Modul ini membahas berbagai bentuk serangan yang paling sering menjebak orang awam, pelaku usaha, dan UMKM. Kita akan melihat bagaimana penipu memanfaatkan emosi, situasi mendesak, dan rasa takut untuk membuat korban menyerahkan akses atau data penting.")

        st.markdown(
            """
            <div class='premium-box'>
                <div class='batch-chip'>Batch 1</div>
                <h4>Social Engineering Dasar</h4>
                <ul>
                    <li>Mengenali modus penipuan yang memanfaatkan emosi dan rasa panik.</li>
                    <li>Mengidentifikasi akun palsu, CS bank tiruan, dan telepon darurat yang menipu.</li>
                    <li>Menyadari bagaimana PIN, OTP, dan password sering diserahkan tanpa sengaja.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='premium-box'>
                <div class='batch-chip'>Batch 2</div>
                <h4>File APK & Malware</h4>
                <ul>
                    <li>Mengetahui bahaya file berformat APK yang dikirim melalui WhatsApp.</li>
                    <li>Mengenali modus tilang palsu, denda pajak, surat sidang, dan suspensi akun toko.</li>
                    <li>Menilai risiko menginstal aplikasi yang tidak resmi.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='premium-box'>
                <div class='batch-chip'>Batch 3</div>
                <h4>Hoaks & Investasi Bodong</h4>
                <ul>
                    <li>Membedakan informasi valid dengan berita hoaks yang tersebar luas.</li>
                    <li>Menolak tawaran keuntungan instan yang berisiko tinggi.</li>
                    <li>Mengenali ciri-ciri penipuan seperti tekanan waktu dan janji hasil cepat.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='premium-box'>
                <div class='batch-chip'>Batch 4</div>
                <h4>Takeover Akun & Verifikasi Ganda</h4>
                <ul>
                    <li>Mencegah akun WhatsApp, email, dan aplikasi bisnis direbut oleh pelaku kejahatan.</li>
                    <li>Menolak memberikan kode OTP 6 digit kepada siapa pun.</li>
                    <li>Mengaktifkan verifikasi dua langkah sebagai pengaman utama.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class='premium-box'>
                <div class='batch-chip'>Batch 5</div>
                <h4>Email, Panggilan Palsu, & Budaya Keamanan</h4>
                <ul>
                    <li>Mengenali email phishing yang tampak profesional.</li>
                    <li>Melawan panggilan dan akun palsu di media sosial.</li>
                    <li>Menumbuhkan budaya keamanan di organisasi dan UMKM agar semua orang lebih waspada.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.success("✅ Tujuan utama dari Modul 1 adalah membangun kebiasaan berpikir kritis: tidak langsung percaya, tidak mudah panik, dan selalu memeriksa kebenaran sebelum memberikan data, uang, atau akses.")

        st.markdown("### 🧭 Prinsip Utama yang Akan Dipelajari")
        st.markdown("1. Menjaga ketenangan dan berpikir kritis saat menerima pesan, panggilan, atau permintaan yang bersifat mendesak atau mengancam.\n2. Verifikasi setiap permintaan data, akses, atau transfer dana melalui kanal resmi yang sudah terkonfirmasi.\n3. Memahami bahwa keamanan siber tidak hanya bergantung pada teknologi, tetapi juga pada keputusan dan kebiasaan manusia.\n4. Membangun sikap skeptis yang sehat terhadap tawaran yang terlalu cepat, terlalu mendesak, atau terlalu menguntungkan untuk menjadi kenyataan.\n5. Melakukan pengecekan berlapis sebelum membagikan informasi sensitif, nomor OTP, password, atau kode akses.")

        st.markdown("### 🏁 Standar Kelulusan Modul 1")
        st.write("Peserta dinyatakan lulus apabila mencapai tingkat keberhasilan 100% pada seluruh 20 materi evaluasi dalam Modul 1. Ketentuan ini dibuat agar pemahaman peserta tidak hanya bersifat parsial, tetapi benar-benar komprehensif, teruji, dan siap diterapkan dalam situasi nyata.")

        st.markdown("### 📸 Contoh Kasus Nyata yang Akan Diulas")
        st.write("Modul ini akan menelaah berbagai skenario penipuan yang sering terjadi dalam kehidupan nyata, seperti akun palsu, pesan pengancam, file APK berbahaya, hoaks keuangan, investasi bodong, dan upaya pengambilalihan akun digital. Setiap kasus akan dikaitkan dengan tindakan pencegahan yang tepat agar peserta mampu mengenali pola serangan dan menahan diri sebelum bertindak.")
        st.write("Dengan pendekatan ini, peserta tidak hanya belajar teori, tetapi juga melatih kemampuan membaca situasi, menilai risiko, dan mengambil keputusan yang aman di tengah tekanan.")

        st.markdown("---")
        
        if st.button("Masuk ke Studi Kasus 1 ➡️", type="primary", use_container_width=True):
            reset_scroll_ke_atas()
            st.session_state.halaman_sekarang = 2
            st.rerun()

    # --- JALUR ENGINE MULTI-MATERI BER-SENSOR SAKTI (MATERI 1 SAMPAI 20) ---
    elif (2 <= st.session_state.halaman_sekarang <= 5) or (7 <= st.session_state.halaman_sekarang <= 10) or (12 <= st.session_state.halaman_sekarang <= 15) or (17 <= st.session_state.halaman_sekarang <= 20) or (22 <= st.session_state.halaman_sekarang <= 25):
        if st.session_state.halaman_sekarang == 2:
            reset_scroll_ke_atas()
            mid, nomor, judul = "m1", 1, "Materi 1: Pengenalan Social Engineering (Sistem vs Manusia)"
            isi_teks = "Pada siang hari, Siti menerima pesan WhatsApp dari nomor yang terlihat seperti layanan resmi marketplace. Isi pesannya menyatakan bahwa akun tokonya akan dibekukan permanen dalam 10 menit karena ada dugaan aktivitas mencurigakan. Dalam pesan itu, tertera kalimat yang menekan: 'Segera verifikasi agar akun Anda tidak ditutup.' Siti sudah panik, karena toko yang ia jalankan baru saja ramai dan ia tidak ingin kehilangan pelanggan. Tanpa mengecek keaslian kanal komunikasi, ia membuka tautan yang dikirim dan masuk ke halaman palsu yang tampak sangat mirip dengan halaman login marketplace. Ia lalu memasukkan password dan kode OTP yang dikirim ke teleponnya. Dalam waktu singkat, pelaku berhasil mengambil alih akun toko dan mencuri saldo penjualan."
            tips_teks = "Jika menerima pesan yang memicu emosi ekstrem (sangat panik/sangat senang), logika Anda sedang dilumpuhkan. Diamkan pesan itu selama 10 menit agar otak kembali tenang."
            soal_teks = "Mengapa pelaku penipuan digital lebih sering mengincar korban manusia secara langsung dibandingkan membobol sistem pertahanan server perbankan/marketplace?"
            opsi_sidang = st.session_state.list_opsi_m1
            next_hal = 3
        
        elif st.session_state.halaman_sekarang == 3:
            mid, nomor, judul = "m2", 2, "Materi 2: Ancaman Pemblokiran Rekening & E-Wallet (Modus Urgency)"
            isi_teks = "Pada pukul 00.30, Pak Budi menerima SMS yang berbunyi: 'AKUN BANK ANDA DIBLOKIR. Verifikasi ulang dalam 2 jam untuk mencegah saldo hangus.' Teks itu terasa sangat menekan karena datang di tengah malam, tepat saat ia sedang memikirkan pembayaran karyawan dan biaya bahan baku. Ia tidak memeriksa apakah SMS itu benar-benar dikirim dari bank resmi. Ia langsung mengeklik tautan yang terlampir dan masuk ke halaman login yang tampak mirip sekali dengan aplikasi bank sebenarnya. Karena ia sudah panik, ia memasukkan PIN, password, dan kode OTP yang masuk ke ponselnya. Esok paginya, ia baru sadar bahwa saldo rekening bisnisnya telah disedot oleh pelaku."
            tips_teks = "Bank resmi tidak pernah menggunakan nomor handphone biasa (+62...) untuk mengirimkan notifikasi pemblokiran akun lewat jalur SMS pribadi nasabah."
            soal_teks = "Anda menerima SMS dari nomor handphone biasa: 'AKUN BANK ANDA DIBLOKIR. Untuk mengaktifkan kembali, silakan verifikasi data Anda di bca-validasi-data.com.' Apa tindakan paling tepat?"
            opsi_sidang = st.session_state.list_opsi_m2
            next_hal = 4

        elif st.session_state.halaman_sekarang == 4:
            mid, nomor, judul = "m3", 3, "Materi 3: Fake CS - Akun WhatsApp Tiruan Berlogo Centang Hijau Palsu"
            isi_teks = "Seorang pemilik warung menerima chat dari nomor yang mengaku sebagai Customer Service bank. Profilnya menggunakan nama yang mirip dengan bank resminya, dan di foto profilnya terlihat ada ceklis hijau kecil yang tampak sangat meyakinkan. Pelaku berkomunikasi dengan bahasa yang sangat profesional, menyebutkan nama lengkap nasabah, dan menahan keraguan korban dengan kata-kata seperti 'kami hanya ingin memastikan akun Anda aman.' Karena korban merasa ditangani secara personal, ia mengirimkan kode OTP yang baru saja masuk ke ponselnya. Setelah itu, pelaku segera masuk ke rekeningnya dan menguras saldo."
            tips_teks = "Akun resmi WhatsApp yang memiliki lencana centang hijau asli, lambang centangnya akan selalu berada di sebelah kanan nama profil akun, bukan diedit menyatu di dalam foto profil bulatan."
            soal_teks = "Bagaimana cara paling akurat untuk membedakan antara akun Customer Service bank resmi dengan akun CS penipu di platform WhatsApp?"
            opsi_sidang = st.session_state.list_opsi_m3
            next_hal = 5

        elif st.session_state.halaman_sekarang == 5:
            mid, nomor, judul = "m4", 4, "Materi 4: Vishing - Telepon Darurat Polisi Palsu & Jebakan Kuras Paylater"
            isi_teks = "Sore itu, seorang ibu menerima telepon dari nomor yang mengaku sebagai polisi. Pelaku menyatakan bahwa anaknya sedang ditangkap karena terlibat dalam perkara serius dan meminta uang tebusan segera agar keadaan bisa diselesaikan. Ia menekan dengan nada keras, menyalahkan ibu tersebut karena tidak cepat membantu, lalu mengancam bahwa jika tidak segera membayar, anaknya akan diproses secara hukum. Ketika ibu menjawab bahwa tabungannya tidak cukup, pelaku lalu memberi instruksi agar ia membuka aplikasi pinjaman online atau layanan Paylater, kemudian memindahkan limit kredit ke nomor rekening yang ia sebutkan. Ibu itu menuruti karena tidak tahu bahwa polisi resmi tidak pernah meminta uang damai lewat telepon atau meminta warga mengaktifkan utang Paylater."
            tips_teks = "Institusi kepolisian resmi tidak pernah meminta uang damai tebusan perkara lewat telepon, dan tidak ada polisi yang menyuruh warga mengaktifkan dana utang Paylater."
            soal_teks = "Seseorang menelepon Anda mengaku sebagai Polisi, menyatakan anak Anda ditangkap. Dia meminta Rp 5 Juta. Saat Anda billing tidak punya uang, dia membimbing Anda untuk membuka aplikasi belanja dan mengaktifkan limit Paylater untuk ditransfer ke dia. Tindakan Anda?"
            opsi_sidang = st.session_state.list_opsi_m4
            next_hal = 6  

        elif st.session_state.halaman_sekarang == 7:
            mid, nomor, judul = "m5", 5, "Materi 5: Bahaya File .APK Kurir - Modus Berkedok Foto Tilang ETLE"
            isi_teks = "Soni sedang mengendarai motor ketika ponselnya menerima pesan WhatsApp dari nomor yang terlihat seperti petugas polisi. Isi pesan itu menyatakan bahwa ia terekam kamera ETLE dan dinyatakan melanggar marka jalan. Dilampirkan juga foto bukti dan link yang berisi file bernama 'Surat_Tilang_Digital.apk' dengan alasan agar ia bisa melihat bukti tilang dan membuktikan bahwa surat tersebut asli. Karena panik dan takut STNK-nya diblokir, Soni langsung mengunduh dan membuka file itu. File tersebut sebenarnya adalah aplikasi berbahaya yang menyadap data login dan kode OTP yang masuk ke ponselnya. Tidak lama kemudian, saldo rekeningnya mulai berkurang tanpa ia ketahui."
            tips_teks = "Pihak Kepolisian RI tidak pernah mengirimkan berkas tilang dalam format APK lewat WhatsApp. Surat resmi selalu berbentuk fisik yang diantar pos tercatat ke rumah."
            st.markdown("### 🖼️ Contoh Screenshot yang Menyerupai Modus Penipuan")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image("images/etle-tilang-1.jpg", caption="Screenshot 1 - Pesan tilang palsu", use_container_width=True)
            with col_img2:
                st.image("images/etle-tilang-2.jpg", caption="Screenshot 2 - Lampiran file APK dalam modus ETLE", use_container_width=True)
            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
            st.markdown("---")
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

                # ----------------- HALAMAN 14: MATERI 13 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 17:
            mid, nomor, judul = "m13", 13, "Materi 13: Takeover Akun - Modus Penipuan Kode OTP WhatsApp Kasir Toko"
            isi_teks = "Seorang kasir toko online menerima chat dari nomor asing yang mengaku sebagai perwakilan resmi WhatsApp pusat. Pelaku menyatakan: 'Kami mendeteksi aktivitas login mencurigakan pada akun toko Anda. Kami baru saja mengirimkan SMS verifikasi 6 angka pelindung ke nomor Anda. Tolong sebutkan angkanya sekarang untuk membatalkan pemblokiran nomor toko.' Karena takut toko kehilangan kontak pelanggan, kasir memberikan 6 angka tersebut. Detik itu juga, akun WhatsApp toko diambil alih pelaku untuk menipu pelanggan Anda."
            tips_teks = "Kode OTP (One-Time Password) 6 angka yang masuk via SMS adalah kunci gembok digital rahasia. Pihak resmi mana pun tidak akan pernah meminta kode tersebut lewat chat pribadi."
            soal_teks = "Seseorang mengaku pihak resmi meminta kode verifikasi 6 angka yang baru saja masuk ke SMS handphone toko Anda. Tindakan proteksi Anda?"
            opsi_sidang = st.session_state.list_opsi_m13
            next_hal = 18

        # ----------------- HALAMAN 15: MATERI 14 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 18:
            mid, nomor, judul = "m14", 14, "Materi 14: Malware Kurir - Modus Berkedok Cek Resi Paket Format .APK"
            isi_teks = "Admin katering menerima chat WhatsApp dari nomor asing yang mengaku sebagai kurir ekspedisi pengantar barang. Pelaku mengirimkan sebuah file dokumen bernama 'Lihat_Foto_Paket_Pesanan.apk' dan berkata: 'Permisi Kak, ada paket bahan makanan katering yang alamatnya kurang jelas. Tolong instal aplikasi resi di bawah ini untuk melihat bukti foto paket and koordinasi pengantaran.' Admin langsung menginstal file tersebut. Malware di dalamnya menyadap SMS OTP bank and menguras rekening modal usaha toko."
            tips_teks = "Ekspedisi resmi selalu menggunakan link pelacakan web resmi atau aplikasi resmi dari Play Store, bukan mengirimkan file mentah berformat .APK lewat WhatsApp personal."
            soal_teks = "Kurir asing mengirimkan file 'Lihat_Foto_Paket_Pesanan.apk' lewat WhatsApp and meminta Anda menginstalnya untuk melacak barang. Tindakan paling aman?"
            opsi_sidang = st.session_state.list_opsi_m14
            next_hal = 19

        # ----------------- HALAMAN 16: MATERI 15 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 19:
            mid, nomor, judul = "m15", 15, "Materi 15: Struk Palsu - Manipulasi Gambar Bukti Transfer Pembeli Grosir"
            isi_teks = "Seorang pembeli memesan katering skala besar senilai Rp10.000.000 and mengirimkan foto kertas struk bukti transfer ATM resmi sebagai tanda bukti pelunasan. Pelaku mendesak agar pesanan katering segera dikirim karena acara akan dimulai. Admin yang percaya langsung mengirimkan pesanan tanpa mengecek mutasi. Sore harinya, pemilik toko menyadari saldo tidak bertambah and struk tersebut adalah hasil editan Photoshop."
            tips_teks = "Jangan pernah memproses pengiriman pesanan besar hanya berdasarkan foto struk fisik atau tangkapan layar bukti transfer pembeli. Wajib verifikasi mutasi uang masuk secara mandiri lewat dasbor m-banking resmi toko."
            soal_teks = "Pembeli mendesak barang dikirim and melampirkan foto struk transfer ATM bernilai besar. Tindakan perlindungan keuangan Anda?"
            opsi_sidang = st.session_state.list_opsi_m15
            next_hal = 20

        # ----------------- HALAMAN 17: MATERI 16 (NEW!) -----------------
        elif st.session_state.halaman_sekarang == 20:
            mid, nomor, judul = "m16", 16, "Materi 16: Benteng Ganda - Aktivasi Fitur Verifikasi Dua Langkah (2FA)"
            isi_teks = "GardaDigital mengenalkan fitur pertahanan siber terkuat untuk tingkat personal awareness, yaitu Two-Factor Authentication (2FA). Dengan mengaktifkan fitur ini, peretas tidak akan pernah bisa mengambil alih akun WhatsApp toko Anda meskipun mereka berhasil mencuri atau menyadap nomor SMS OTP Anda, karena sistem akan meminta kode PIN rahasia tambahan yang hanya diketahui oleh kepala pemilik toko."
            tips_teks = "Aktifkan Verifikasi Dua Langkah di menu Pengaturan -> Akun -> Verifikasi Dua Langkah di aplikasi WhatsApp operasional bisnis Anda sekarang juga."
            soal_teks = "Langkah teknis paling akurat untuk mengunci akun WhatsApp toko Anda agar anti-pembajakan meskipun nomor OTP Anda bocor?"
            opsi_sidang = st.session_state.list_opsi_m16
            next_hal = 21  # Rapor Batch 4 (M13-16) sebelum lanjut ke Batch 5

        # ================= MATERI 17-20 (BATCH 5: SOCIAL ENGINEERING LANJUTAN UMKM) =================
        elif st.session_state.halaman_sekarang == 22:
            mid, nomor, judul = "m17", 17, "Materi 17: Phishing Email Massal - Jebakan Invoice & Verifikasi Data Supplier"
            isi_teks = "Admin toko katering menerima email dari alamat 'supp-lier-terpercaya@supplier-ternama.com' (mirip sekali dengan supplier asli yang biasanya melayani toko) yang isinya menyuruh update data rekening 'untuk efisiensi pembayaran cicilan'. Email tersebut dilampirkan invoice palsu dan link untuk 'verifikasi akun'. Karena terburu-buru dan email terlihat profesional, admin langsung klik link dan memasukkan username dan password e-banking toko. Detik itu juga, peretas masuk akun m-banking dan menguras saldo modal toko dalam hitungan menit."
            tips_teks = "Supplier resmi tidak pernah meminta update data sensitif via email atau link. Selalu panggil supplier langsung menggunakan nomor di invoice resmi atau website resmi mereka untuk konfirmasi."
            soal_teks = "Anda menerima email dari alamat mirip supplier yang minta update data rekening via link attachment. Tindakan paling aman?"
            opsi_sidang = st.session_state.list_opsi_m17
            next_hal = 23

        elif st.session_state.halaman_sekarang == 23:
            mid, nomor, judul = "m18", 18, "Materi 18: Pretext Calling - Telepon Tipuan Menyamar Supplier/Bank/Kurir"
            isi_teks = "Pemilik warung SOHO menerima telepon dari nomor yang terlihat profesional. Si penelepon berbicara cepat dan serius, menyamar sebagai petugas dari bank toko dan berkata: 'Ibu, karena terindikasi aktivitas mencurigakan pada akun bisnis Anda, kami harus update data segera. Tolong berikan nomor rekening, password, dan kode OTP terakhir Anda untuk verifikasi keamanan.' Karena panik and terburu-buru melayani pelanggan, pemilik langsung memberikan informasi tersebut. Dalam hitungan jam, saldo tabungan toko berhasil ditarik dan digunakan untuk membeli voucher game."
            tips_teks = "Bank resmi tidak pernah meminta password, OTP, atau data sensitif via telepon. Pihak resmi akan selalu meminta Anda mengecek langsung melalui website resmi atau datang ke kantor cabang. Selalu verifikasi identitas penelepon dengan call-back ke nomor resmi."
            soal_teks = "Si penelepon yang terlihat profesional dan urgent meminta password e-banking. Tindakan paling aman?"
            opsi_sidang = st.session_state.list_opsi_m18
            next_hal = 24

        elif st.session_state.halaman_sekarang == 24:
            mid, nomor, judul = "m19", 19, "Materi 19: Impersonation Media Sosial - Akun Palsu di WhatsApp, Instagram, Facebook"
            isi_teks = "Pemilik toko katering yang terkenal di Instagram melihat ada akun baru yang mirip sekali dengan profilnya: foto profil sama, nama serupa (hanya beda 1 huruf), dan sudah memiliki ribuan followers. Akun palsu itu mulai mengirim pesan ke ribuan follower toko yang asli, mengaku sedang promo potongan harga 50% dan minta pembeli langsung transfer ke rekening pribadinya. Banyak pelanggan yang tertipu dan transfer uang. Korban baru menyadari setelah melihat komplain pelanggan bahwa akun itu adalah imposter yang mencuri reputasi tokonya."
            tips_teks = "Verifikasi akun sebelum berbisnis: cek follow-back ke akun resmi, lihat konsistensi posting, hubungi langsung via akun resmi untuk konfirmasi. Jangan percaya akun baru meski mirip. Laporkan akun imposter ke tim support platform segera."
            soal_teks = "Ada akun baru mirip toko Anda yang mulai menipu pelanggan dengan promo palsu. Tindakan paling tepat?"
            opsi_sidang = st.session_state.list_opsi_m19
            next_hal = 25

        elif st.session_state.halaman_sekarang == 25:
            mid, nomor, judul = "m20", 20, "Materi 20: Social Engineering Awareness - Edukasi & Deteksi Dini untuk UMKM"
            isi_teks = "Banyak UMKM mengira social engineering hanya terjadi pada perusahaan besar atau orang kaya. Faktanya, UMKM dan SOHO adalah target utama karena sistem keamanan lebih lemah, staf kurang training, dan pemilik lebih mudah panik ketika ada tekanan urgent. Contoh: kasir yang baru dapat telepon urgent mengirim Rp 5 juta tanpa konfirmasi ke pemilik, atau admin yang klik link phishing tanpa tanya-tanya. Solusi terbaik adalah edukasi rutin untuk semua staf (tidak hanya pimpinan) dan membangun budaya 'bertanya dulu sebelum bertindak' ketika ada permintaan data sensitif atau uang dalam situasi urgent."
            tips_teks = "Buat checklist verifikasi: (1) Siapa yang minta? (2) Minta apa? (3) Via channel apa? (4) Ada urgency/tekanan? Jika ragu, hubungi pemilik/supervisor dulu sebelum memberikan data/uang. Ingatkan: pihak resmi tidak pernah urgent-urgent tentang uang."
            soal_teks = "Bagaimana cara membangun kesadaran keamanan digital di seluruh tim UMKM Anda?"
            opsi_sidang = st.session_state.list_opsi_m20
            next_hal = 26
        
        else:
            st.error("❌ Halaman tidak valid. Arahkan ulang ke beranda.")
            if st.button("Kembali ke Beranda", type="primary", use_container_width=True):
                st.session_state.halaman_sekarang = 0
                st.rerun()
            st.stop()

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
            
            teks_lanjut = f"Materi Selanjutnya (Materi {nomor + 1}) ➡️" if nomor not in [4, 8, 12, 16, 20] else "Buka Halaman Rapor Evaluasi Akhir 📊"
            if st.button(teks_lanjut, use_container_width=True):
                # UPDATE RECORD HALAMAN TERAKHIR KE DATABASE SEBELUM BERPINDAH
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET halaman_terakhir = ? WHERE email = ?", (next_hal, st.session_state.user_email))
                conn.commit()
                conn.close()
                
                st.session_state.halaman_sekarang = next_hal
                st.rerun()

    # --- HALAMAN 21: RAPOR BATCH 4 (MATERI 13-16 SEBELUM LANJUT KE BATCH 5) ---
    elif st.session_state.halaman_sekarang == 21:
        st.markdown("### 📊 Rapor Batch 4: Evaluasi Materi 13-16 (Takeover Akun & Authentication)")
        st.write("Selamat menyelesaikan Batch 4! Berikut adalah hasil evaluasi Anda untuk materi 13-16 tentang perlindungan akun dan autentikasi ganda:")
        
        skor_b4 = sum([1 for m_id in ["m13", "m14", "m15", "m16"] if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]])
        salah_b4 = 4 - skor_b4
        
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        cursor.execute("SELECT remidi_b4 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        
        total_remidi_b4 = data_remidi[0] if data_remidi else 0
        
        st.metric("Jumlah Upaya Percobaan Batch 4", f"{total_remidi_b4} Kali")
        st.markdown("---")

        col_t1, col_t2, col_t3 = st.columns([1, 2, 1])
        with col_t2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:13px;'>🎯 Grafik Akurasi Jawaban Batch 4 (M13-16)</p>", unsafe_allow_html=True)
            fig_b4, ax_b4 = plt.subplots(figsize=(3, 3))
            ax_b4.pie([skor_b4, salah_b4], labels=[f"Aman ({skor_b4})", f"Celah ({salah_b4})"], colors=['#2ECC71', '#E74C3C'], autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':8})
            ax_b4.axis('equal')
            fig_b4.patch.set_alpha(0)
            ax_b4.set_facecolor('none')
            st.pyplot(fig_b4)

        st.markdown("---")
        if skor_b4 == 4:
            st.success("👑 **STATUS BATCH 4: LULUS TOTAL (4/4)**\n\nGerbang kurikulum lanjutan Batch 5 (Social Engineering Lanjutan untuk UMKM) resmi dibuka!")
            
            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE pengguna SET status_lulus_b4 = 1 WHERE email = ?", (st.session_state.user_email,))
            conn.commit()
            conn.close()
            
            if st.button("Maju ke Batch 5: Social Engineering Lanjutan untuk UMKM (Materi 17) 🔓🚀", type="primary", use_container_width=True):
                st.session_state.halaman_sekarang = 22
                st.rerun()
        else:
            st.error(f"🚨 **STATUS BATCH 4: WAJIB REMIDI ({skor_b4}/4 BENAR)**\n\nSelesaikan remedial ujian Batch 4 sampai sempurna untuk melanjutkan!")
            if st.button("🔄 Ulangi Ujian Batch 4 (Urutan Kalimat di-Shuffle Kembali 🎲)", type="primary", use_container_width=True):
                conn = sqlite3.connect("gardadigital.db")
                cursor = conn.cursor()
                cursor.execute("UPDATE pengguna SET remidi_b4 = remidi_b4 + 1 WHERE email = ?", (st.session_state.user_email,))
                conn.commit()
                conn.close()
                
                for mid in ["m13", "m14", "m15", "m16"]:
                    if mid in st.session_state.materi_selesai: st.session_state.materi_selesai.remove(mid)
                    if mid in st.session_state.jawaban_user: del st.session_state.jawaban_user[mid]
                    if mid in st.session_state.pilihan_text_save: del st.session_state.pilihan_text_save[mid]
                
                random.shuffle(st.session_state.list_opsi_m13)
                random.shuffle(st.session_state.list_opsi_m14)
                random.shuffle(st.session_state.list_opsi_m15)
                random.shuffle(st.session_state.list_opsi_m16)
                st.session_state.halaman_sekarang = 17  # Balik ke Materi 13
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
            fig1.patch.set_alpha(0)
            ax1.set_facecolor('none')
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
            fig_final.patch.set_alpha(0)
            ax_final.set_facecolor('none')
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
            fig_b3.patch.set_alpha(0)
            ax_b3.set_facecolor('none')
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

    # --- HALAMAN 26: RAPOR AKHIR KOMPREHENSIF (SEMUA 20 MATERI) & SERTIFIKAT DIGITAL ---
    elif st.session_state.halaman_sekarang == 26:
        st.markdown("### 📊 Rapor Akhir Evaluasi Komprehensif: Lulus Total GardaDigital Modul 1 (Materi 1 - 20)")
        st.write("🎉 Luar biasa! Anda telah menyelesaikan 20 materi lengkap pelatihan keamanan siber GardaDigital Modul 1. Berikut adalah analisis mendalam dan komprehensif tentang ketahanan siber akal sehat Anda:")
        st.markdown("---")
        
        # 1. HITUNG SKOR KOMULATIF LENGKAP (TOTAL DARI 20 MATERI)
        skor_komulatif = 0
        for m_id in ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13", "m14", "m15", "m16", "m17", "m18", "m19", "m20"]:
            if st.session_state.jawaban_user.get(m_id) == KUNCI_MATERI[m_id]:
                skor_komulatif += 1
        salah_komulatif = 20 - skor_komulatif

        # Tarik data status kelulusan and remidi dari database SQLite
        conn = sqlite3.connect("gardadigital.db")
        cursor = conn.cursor()
        try: cursor.execute("ALTER TABLE pengguna ADD COLUMN remidi_b5 INTEGER DEFAULT 0"); conn.commit()
        except sqlite3.OperationalError: pass
        try: cursor.execute("ALTER TABLE pengguna ADD COLUMN status_lulus_b5 INTEGER DEFAULT 0"); conn.commit()
        except sqlite3.OperationalError: pass
        try: cursor.execute("ALTER TABLE pengguna ADD COLUMN tanggal_lulus TEXT"); conn.commit()
        except sqlite3.OperationalError: pass
        
        cursor.execute("SELECT remidi_b1, remidi_b2, remidi_b3, remidi_b4, remidi_b5 FROM pengguna WHERE email = ?", (st.session_state.user_email,))
        data_remidi = cursor.fetchone()
        conn.close()
        
        r1 = data_remidi[0] if data_remidi else 0
        r2 = data_remidi[1] if data_remidi else 0
        r3 = data_remidi[2] if data_remidi else 0
        r4 = data_remidi[3] if data_remidi else 0
        r5 = data_remidi[4] if data_remidi else 0

        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1: st.metric("Remidi B1", f"{r1} Kali")
        with col_m2: st.metric("Remidi B2", f"{r2} Kali")
        with col_m3: st.metric("Remidi B3", f"{r3} Kali")
        with col_m4: st.metric("Remidi B4", f"{r4} Kali")
        with col_m5: st.metric("Remidi B5", f"{r5} Kali")
        st.markdown("---")

        # 2. VISUALISASI PIE CHART BESAR DI TENGAH
        col_tengah1, col_tengah2, col_tengah3 = st.columns([1, 2, 1])
        with col_tengah2:
            st.markdown("<p style='text-align: center; font-weight: bold; font-size:14px;'>🎯 Grafik Akurasi Komulatif: Seluruh Kurikulum Modul 1 (20 Materi Lengkap)</p>", unsafe_allow_html=True)
            fig_final, ax_final = plt.subplots(figsize=(3.5, 3.5))
            colors_pie = ['#27AE60', '#E74C3C'] if skor_komulatif >= 18 else ['#F39C12', '#E74C3C'] if skor_komulatif >= 15 else ['#E74C3C', '#95A5A6']
            ax_final.pie([skor_komulatif, salah_komulatif], labels=[f"Benar ({skor_komulatif}/20)", f"Salah ({salah_komulatif}/20)"], colors=colors_pie, autopct='%1.1f%%', startangle=90, textprops={'color':"white", 'fontsize':10, 'weight':'bold'})
            ax_final.axis('equal')
            fig_final.patch.set_alpha(0)
            ax_final.set_facecolor('none')
            st.pyplot(fig_final)

        st.markdown("---")
        
        # 3. BREAKDOWN SKOR PER BATCH
        st.markdown("#### 📈 Rincian Skor Per Batch Pelatihan:")
        batch_scores = {
            "Batch 1 (M1-4): Social Engineering Dasar": sum([1 for m in ["m1", "m2", "m3", "m4"] if st.session_state.jawaban_user.get(m) == KUNCI_MATERI.get(m)]),
            "Batch 2 (M5-8): File APK & Malware": sum([1 for m in ["m5", "m6", "m7", "m8"] if st.session_state.jawaban_user.get(m) == KUNCI_MATERI.get(m)]),
            "Batch 3 (M9-12): Hoaks & Penipuan Investasi": sum([1 for m in ["m9", "m10", "m11", "m12"] if st.session_state.jawaban_user.get(m) == KUNCI_MATERI.get(m)]),
            "Batch 4 (M13-16): Takeover & Authentication": sum([1 for m in ["m13", "m14", "m15", "m16"] if st.session_state.jawaban_user.get(m) == KUNCI_MATERI.get(m)]),
            "Batch 5 (M17-20): Infrastruktur & Governance": sum([1 for m in ["m17", "m18", "m19", "m20"] if st.session_state.jawaban_user.get(m) == KUNCI_MATERI.get(m)])
        }
        
        for batch_name, batch_score in batch_scores.items():
            status_badge = "✅" if batch_score == 4 else "⚠️" if batch_score >= 2 else "❌"
            st.write(f"{status_badge} {batch_name}: **{batch_score}/4 Benar**")
        
        st.markdown("---")
        
        # 4. LOGIKA KELULUSAN FINAL - HANYA LULUS JIKA SEMUA 20 BENAR
        if skor_komulatif == 20:
            st.balloons() 
            st.success(f"👑 **SELAMAT! ANDA TELAH LULUS SEMPURNA GardaDigital MODUL 1!**\n\n🏆 **SKOR AKHIR: 20/20 BENAR (100%)**\n\nLuar biasa, {st.session_state.user_email}! Anda telah menguasai semua aspek keamanan siber mulai dari taktik manipulasi sosial, malware, hoaks, hingga infrastruktur dan budaya keamanan organisasi. Anda kini berhak mendapatkan sertifikat digital keamanan siber Modul 1 dari GardaDigital yang diakui secara nasional. Bisnis toko online, keuangan, dan data pelanggan Anda terlindungi maksimal dengan kesadaran dan disiplin keamanan tingkat tinggi!")
            
            # Kunci kelulusan final ke database
            from datetime import datetime
            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE pengguna SET status_lulus_b5 = 1, halaman_terakhir = 25, tanggal_lulus = ? WHERE email = ?", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), st.session_state.user_email))
            conn.commit()
            conn.close()
            
            st.markdown("---")
            st.markdown("### 🎓 Sertifikat Digital Keamanan Siber")
            st.markdown(f"**Nama Peserta:** {st.session_state.user_email}")
            st.markdown("**Modul:** GardaDigital Modul 1 - Social Engineering & Pertahanan Siber")
            st.markdown(f"**Skor Akhir:** 20/20 (100% Sempurna)")
            st.markdown(f"**Tanggal Kelulusan:** {datetime.now().strftime('%d %B %Y')}")
            st.markdown("---")

            conn = sqlite3.connect("gardadigital.db")
            cursor = conn.cursor()
            cursor.execute("SELECT nama_depan, nama_belakang, instansi FROM pengguna WHERE email = ?", (st.session_state.user_email,))
            data_peserta = cursor.fetchone()
            conn.close()

            nama_lengkap = "Peserta"
            instansi = "Umum"
            if data_peserta:
                nama_lengkap = f"{data_peserta[0] or ''} {data_peserta[1] or ''}".strip() or st.session_state.user_email
                instansi = data_peserta[2] or "Umum"

            if st.button("🎖️ TERBITKAN SERTIFIKAT DIGITAL ANDA SEKARANG", type="primary", use_container_width=True):
                if REPORTLAB_READY:
                    pdf_bytes = buat_sertifikat_modul1_pdf(nama_lengkap, instansi, datetime.now().strftime("%d %B %Y"))
                    if pdf_bytes:
                        st.download_button(
                            label="⬇️ Unduh Sertifikat Modul 1 (PDF)",
                            data=pdf_bytes,
                            file_name=f"sertifikat_gardadigital_modul1_{nama_lengkap.replace(' ', '_').lower()}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )
                        st.success("✅ Sertifikat Anda siap diunduh.")
                    else:
                        st.warning("⚠️ Library ReportLab belum tersedia di lingkungan ini. Sertifikat PDF belum bisa dibuat.")
                else:
                    st.warning("⚠️ Library ReportLab belum tersedia di lingkungan ini. Sertifikat PDF belum bisa dibuat.")
                
        else:
            skor_persen = (skor_komulatif / 20) * 100
            if skor_persen >= 75:
                st.warning(f"⚠️ **STATUS: LULUS DENGAN CATATAN ({skor_komulatif}/20 BENAR = {skor_persen:.1f}%)**\n\nAnda telah menguasai sebagian besar materi, namun masih ada celah keamanan yang perlu ditutup. Silakan review materi yang masih kurang sempurna.")
                if st.button("🔍 Review Materi & Remedial", type="primary", use_container_width=True):
                    st.session_state.halaman_sekarang = 0
                    st.rerun()
            else:
                st.error(f"🚨 **STATUS: BELUM LULUS ({skor_komulatif}/20 BENAR = {skor_persen:.1f}%)**\n\nAnda masih memiliki banyak celah keamanan yang perlu ditutup. Sistem keamanan toko Anda masih sangat rentan. Silakan ulangi ujian dari materi yang belum dikuasai.")
                if st.button("🔄 Ulangi Ujian Dari Awal (Batch 1)", type="primary", use_container_width=True):
                    conn = sqlite3.connect("gardadigital.db")
                    cursor = conn.cursor()
                    cursor.execute("UPDATE pengguna SET remidi_b5 = remidi_b5 + 1, halaman_terakhir = 2 WHERE email = ?", (st.session_state.user_email,))
                    conn.commit()
                    conn.close()
                    
                    for mid in ["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10", "m11", "m12", "m13", "m14", "m15", "m16", "m17", "m18", "m19", "m20"]:
                        if mid in st.session_state.materi_selesai: 
                            st.session_state.materi_selesai.remove(mid)
                        if mid in st.session_state.jawaban_user: 
                            del st.session_state.jawaban_user[mid]
                        if mid in st.session_state.pilihan_text_save: 
                            del st.session_state.pilihan_text_save[mid]
                    
                    st.session_state.halaman_sekarang = 2
                    st.rerun()
