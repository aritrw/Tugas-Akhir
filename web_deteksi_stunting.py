import streamlit as st
import numpy as np
import pickle
import pandas as pd
import sqlite3
import hashlib
import io
from datetime import datetime
import warnings

# Suppress sklearn version warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# Konfigurasi halaman
st.set_page_config(
    page_title="Prediksi Stunting - Petugas Kesehatan", 
    layout="wide", 
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# CSS styling yang lebih modern dan user-friendly
st.markdown("""
<style>

    /* ====== BACKGROUND ====== */
    .stApp {
        background-image: url('https://raw.githubusercontent.com/aritrw/Tugas-Akhir/1a1911030302522c97958bd265f696ed89ac0c76/61808.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #1e2a38;
    }

    /* ===== HEADER UTAMA TANPA BOX ===== */
    .header-container {
        background: transparent !important;    /* hilangkan kotak */
        box-shadow: none !important;
        border: none !important;
        padding: 3rem 1rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }

    /* ====== TITLE ====== */
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #0f4c81; /* biru gelap lebih kontras */
        text-shadow: 0px 1px 3px rgba(0,0,0,0.15);
        margin-bottom: 0.5rem;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #28527a;
        font-weight: 400;
    }

    /* ====== SUB HEADER FORM ====== */
    .form-container h3,
    .form-container h2 {
        color: #0f4c81;
        font-weight: 700;
    }

    /* ====== INPUT FIELDS ====== */
    input, select, textarea {
        border-radius: 10px !important;
        border: 2px solid #d6dce5 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        background: rgba(255,255,255,0.9) !important;
        color: #1e2a38 !important;
    }

    input:focus, select:focus {
        border-color: #2e89ff !important;
        box-shadow: 0 0 6px rgba(46,137,255,0.4) !important;
    }
    
    /* ====== INPUT FIELDS ====== */

    /* Hilangkan SEMUA shadow/border default Streamlit di semua level */
    div[data-testid="stTextInput"],
    div[data-testid="stPasswordInput"],
    div[data-testid="stNumberInput"],
    div[data-testid="stTextInput"] > div,
    div[data-testid="stPasswordInput"] > div,
    div[data-testid="stNumberInput"] > div,
    div[data-testid="stTextInput"] > div > div,
    div[data-testid="stPasswordInput"] > div > div,
    div[data-testid="stNumberInput"] > div > div {
        box-shadow: none !important;
        border: none !important;
        background: transparent !important;
    }

    /* Styling input SAMA PERSIS dengan jabatan */
    div[data-testid="stTextInput"] > div > div > input,
    div[data-testid="stPasswordInput"] > div > div > input,
    div[data-testid="stNumberInput"] > div > div > input {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid #d6dce5 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        color: #1e2a38 !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
        -moz-box-shadow: none !important;
    }

    /* Hover state - sama dengan jabatan */
    div[data-testid="stTextInput"] > div > div > input:hover,
    div[data-testid="stPasswordInput"] > div > div > input:hover,
    div[data-testid="stNumberInput"] > div > div > input:hover {
        border-color: #2e89ff !important;
        box-shadow: none !important;
    }

    /* Focus state - sama dengan jabatan */
    div[data-testid="stTextInput"] > div > div > input:focus,
    div[data-testid="stPasswordInput"] > div > div > input:focus,
    div[data-testid="stNumberInput"] > div > div > input:focus {
        border-color: #2e89ff !important;
        box-shadow: 0 0 6px rgba(46,137,255,0.4) !important;
        background: rgba(255,255,255,0.9) !important;
        outline: none !important;
    }

    /* General input styling */
    input, select, textarea {
        border-radius: 10px !important;
        border: 2px solid #d6dce5 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        background: rgba(255,255,255,0.9) !important;
        color: #1e2a38 !important;
        box-shadow: none !important;
        -webkit-box-shadow: none !important;
        -moz-box-shadow: none !important;
    }

    input:focus, select:focus, textarea:focus {
        border-color: #2e89ff !important;
        box-shadow: 0 0 6px rgba(46,137,255,0.4) !important;
        outline: none !important;
    }
        
        /* ====== SELECTBOX STYLING - SAMA DENGAN FIELD LAIN ====== */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.9) !important;
        border: 2px solid #d6dce5 !important;
        border-radius: 10px !important;
        color: #1e2a38 !important;
        padding: 0.75rem 1rem !important;
    }

    /* Hilangkan kotak putih input di dalam selectbox */
    div[data-baseweb="select"] input {
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        position: absolute !important;
    }

    /* Hilangkan border/background input field */
    div[data-baseweb="select"] > div > div:first-child {
        background: transparent !important;
        border: none !important;
    }

    div[data-baseweb="select"] > div:hover {
        border-color: #2e89ff !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #2e89ff !important;
        box-shadow: 0 0 6px rgba(46,137,255,0.4) !important;
    }

    /* Teks yang dipilih dalam selectbox */
    div[data-baseweb="select"] span {
        color: #1e2a38 !important;
    }

    /* Dropdown arrow */
    div[data-baseweb="select"] svg {
        color: #1e2a38 !important;
    }

    /* Dropdown menu saat dibuka */
    div[role="listbox"] {
        background: rgba(255,255,255,0.98) !important;
        border: 2px solid #d6dce5 !important;
        border-radius: 10px !important;
    }

    /* Item dalam dropdown */
    div[role="option"] {
        color: #1e2a38 !important;
        background: transparent !important;
        padding: 0.75rem 1rem !important;
    }

    div[role="option"]:hover {
        background: rgba(46,137,255,0.1) !important;
    }

    /* ====== FIX TEXT TERPILIH - POSISI PAS ====== */
    div[data-baseweb="select"] > div {
        padding: 0.6rem 1rem !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Pastikan container value terlihat penuh */
    div[data-baseweb="select"] > div > div {
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }

    /* Value container tanpa padding extra */
    div[data-baseweb="select"] > div > div > div {
        padding: 0 !important;
        margin: 0 !important;
        overflow: visible !important;
        white-space: nowrap !important;
        line-height: normal !important;
    }

    /* Text value yang terpilih */
    div[data-baseweb="select"] span {
        overflow: visible !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
    }

    /* Pastikan input yang di-hide tidak ganggu layout */
    div[data-baseweb="select"] input {
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        position: absolute !important;
    }


    /* ====== PLACEHOLDER SELECTBOX ====== */
    div[data-baseweb="select"] [aria-selected="false"] {
        color: #444 !important;
        opacity: 1 !important;
    }

    /* Placeholder text untuk selectbox */
    div[data-baseweb="select"] > div > div > div {
        color: #444 !important;
    }

    /* Ketika ada nilai terpilih, warna jadi gelap */
    div[data-baseweb="select"] [aria-selected="true"] {
        color: #1e2a38 !important;
    }

    /* Samakan padding dengan field lain - hilangkan padding extra internal */
    div[data-baseweb="select"] > div {
        padding: 0.75rem 1rem !important;
    }

    /* Hilangkan padding internal yang bikin text maju */
    div[data-baseweb="select"] > div > div {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Value container tanpa padding extra */
    div[data-baseweb="select"] > div > div > div {
        padding: 0 !important;
        margin: 0 !important;
    }

    /* ====== BUTTON STYLING (BACKGROUND HITAM TETAP, HANYA TEKS BERUBAH) ====== */
    .stButton > button,
    button[kind="primary"],
    button[kind="secondary"],
    div[data-testid="stForm"] button {
        background: #2b2b2b !important; /* Background hitam gelap */
        color: white !important; /* Teks putih saat normal */
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3) !important;
    }
    
    .stButton > button:hover,
    button[kind="primary"]:hover,
    button[kind="secondary"]:hover,
    div[data-testid="stForm"] button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.5) !important;
        background: #2b2b2b !important; /* Background tetap hitam */
        color: #4ac5b8 !important; /* Teks jadi tosca/teal terang saat hover */
    }
    
    /* Pastikan teks button selalu terlihat */
    .stButton > button p,
    button[kind="primary"] p,
    button[kind="secondary"] p {
        color: inherit !important;
    }


    /* ====== DANGER BUTTON ====== */
    .delete-button,
    .stButton > button[kind="danger"] {
        background: linear-gradient(135deg, #ff3c3c, #d11a2a) !important;
        box-shadow: 0px 6px 18px rgba(255, 60, 60, 0.35);
    }

    /* ====== USER INFO TOP ====== */
    .user-info {
        background: linear-gradient(135deg, #4ac5b8, #3aa89c);
        padding: 1.2rem;
        color: white;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0px 6px 20px rgba(74, 197, 184, 0.4);
    }

    /* ====== STAT CARDS ====== */
    .stat-card {
        background: rgba(255,255,255,0.95);
        padding: 1.3rem;
        border-radius: 14px;
        text-align: center;
        box-shadow: 0px 3px 12px rgba(0,0,0,0.1);
        border: 1px solid #eaeaea;
    }

    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #176beb;
    }

    .stat-label {
        font-size: 0.9rem;
        color: #4a5c75;
    }

    /* ====== ALERT BOX (ASLI) ====== */
    .stSuccess > div,
    .stError > div,
    .stWarning > div,
    .stInfo > div {
        border-radius: 12px;
        padding: 1.2rem;
        font-size: 1rem;
        font-weight: 500;
    }

    /* ======================================================
       ===== LABEL JADI WARNA HITAM ========
       ====================================================== */

    .stTextInput label,
    .stPasswordInput label,
    .stSelectbox label,
    .stNumberInput label {
        color: #000 !important;
        font-weight: 700 !important;
        text-shadow: none !important;
    }

    input::placeholder {
        color: #444 !important;
        opacity: 1 !important;
    }
    
    /* ======================================================
       ===== PERBAIKAN ALERT AGAR JELAS (SEMUA TIPE) ========
       ====================================================== */

    /* Semua alert (warning, error, success, info) */
    .stAlert > div[role="alert"] {
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        background-color: rgba(255, 193, 7, 0.97) !important;  /* kuning solid */
        color: #3d3d3d !important;
        border-left: 6px solid #c69500 !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2) !important;
    }
    
    /* ===== ANIMASI FADE IN DAN FADE OUT ===== */
    @keyframes fadeAlert {
        0% { opacity: 0; transform: translateY(-5px); }
        10% { opacity: 1; transform: translateY(0); }
        90% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-5px); }
    }

    /* Terapkan animasi ke semua alert */
    .stAlert > div[role="alert"] {
        animation: fadeAlert 2s ease-in-out forwards !important;
    }
    
        /* ====== HASIL PREDIKSI TANPA FADE ====== */
    .result-alert {
        border-radius: 12px !important;
        padding: 1.2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.2) !important;
        margin-bottom: 0.8rem !important;
    }

    .result-alert-risk {
        background-color: rgba(255, 99, 71, 0.97) !important;   /* merah tomat */
        color: #3d3d3d !important;
        border-left: 6px solid #b71c1c !important;
    }

    .result-alert-safe {
        background-color: rgba(46, 213, 115, 0.97) !important;  /* hijau */
        color: #0b2e13 !important;
        border-left: 6px solid #1b5e20 !important;
    }

    /*  ==============================
         TABEL RINGKASAN DATA ANAK
        ============================== */

    div[data-testid="stTable"] {
        background-color: rgba(255, 255, 255, 0.96) !important;
        padding: 1rem !important;
        border-radius: 16px !important;
        box-shadow: 0px 4px 16px rgba(0,0,0,0.12) !important;
    }

    /* Table container */
    div[data-testid="stTable"] table {
        width: 100% !important;
        border-collapse: collapse !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* HEADER saja */
    div[data-testid="stTable"] thead th {
        background-color: #0f4c81 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
        font-size: 1rem !important;
    }

    /* INDEX / kolom "Parameter" di BODY -> th di tbody */
    div[data-testid="stTable"] tbody th {
        background-color: #ffffff !important;
        color: #1e2a38 !important;
        font-weight: 600 !important;
        padding: 10px 14px !important;
        font-size: 1rem !important;
    }

    /* Sel nilai (kolom kanan) */
    div[data-testid="stTable"] tbody td {
        background-color: #ffffff !important;
        color: #1e2a38 !important;
        padding: 10px 14px !important;
        border-bottom: 1px solid #e5e8ef !important;
        font-size: 1rem !important;
    }

    /* Zebra row biar manis */
    div[data-testid="stTable"] tbody tr:nth-child(even) th,
    div[data-testid="stTable"] tbody tr:nth-child(even) td {
        background-color: #f7f9fc !important;
    }

    /* Last row tanpa border bawah */
    div[data-testid="stTable"] tbody tr:last-child td,
    div[data-testid="stTable"] tbody tr:last-child th {
        border-bottom: none !important;
    }
    

</style>
""", unsafe_allow_html=True)


# Fungsi untuk hash password
def hash_password(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Fungsi untuk verifikasi password
def verify_password(password, hashed):
    return hash_password(password) == hashed

# Inisialisasi database
def init_database():
    conn = sqlite3.connect('stunting_app.db')
    c = conn.cursor()
    
    # Tabel untuk users (petugas kesehatan)
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nama_lengkap TEXT NOT NULL,
        jabatan TEXT,
        instansi TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Tabel untuk prediksi stunting (dimodifikasi dengan user_id)
    c.execute('''
    CREATE TABLE IF NOT EXISTS prediksi_stunting (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        Nama TEXT,
        Nama_Ayah TEXT,
        Nama_Ibu TEXT,
        Jenis_Kelamin TEXT,
        Usia INTEGER,
        BB_Lahir REAL,
        TB_Lahir REAL,
        BB_Sekarang REAL,
        TB_Sekarang REAL,
        hasil_prediksi TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    conn.commit()
    conn.close()

# Fungsi registrasi
def register_user(username, password, nama_lengkap, jabatan, instansi):
    conn = sqlite3.connect('stunting_app.db')
    c = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        c.execute('''
        INSERT INTO users (username, password, nama_lengkap, jabatan, instansi)
        VALUES (?, ?, ?, ?, ?)
        ''', (username, hashed_password, nama_lengkap, jabatan, instansi))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

# Fungsi login
def login_user(username, password):
    conn = sqlite3.connect('stunting_app.db')
    c = conn.cursor()
    
    c.execute('SELECT id, password, nama_lengkap, jabatan, instansi FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user[1]):
        return {
            'id': user[0],
            'username': username,
            'nama_lengkap': user[2],
            'jabatan': user[3],
            'instansi': user[4]
        }
    return None

# Fungsi untuk mendapatkan statistik user
def get_user_statistics(user_id):
    conn = sqlite3.connect('stunting_app.db')
    c = conn.cursor()
    
    # Total prediksi
    c.execute('SELECT COUNT(*) FROM prediksi_stunting WHERE user_id = ?', (user_id,))
    total_prediksi = c.fetchone()[0]
    
    # Prediksi berisiko
    c.execute('SELECT COUNT(*) FROM prediksi_stunting WHERE user_id = ? AND hasil_prediksi = "Berisiko stunting"', (user_id,))
    berisiko = c.fetchone()[0]
    
    # Prediksi tidak berisiko
    tidak_berisiko = total_prediksi - berisiko
    
    conn.close()
    
    return {
        'total_prediksi': total_prediksi,
        'berisiko': berisiko,
        'tidak_berisiko': tidak_berisiko
    }

# Fungsi untuk menghapus semua riwayat prediksi user
def delete_all_predictions(user_id):
    conn = sqlite3.connect('stunting_app.db')
    c = conn.cursor()
    
    c.execute('DELETE FROM prediksi_stunting WHERE user_id = ?', (user_id,))
    affected_rows = c.rowcount
    conn.commit()
    conn.close()
    
    return affected_rows

# Fungsi untuk mendapatkan riwayat terbaru
def get_recent_predictions(user_id, limit=5):
    conn = sqlite3.connect('stunting_app.db')
    c = conn.cursor()
    c.execute('''
    SELECT nama, hasil_prediksi, created_at 
    FROM prediksi_stunting 
    WHERE user_id = ? 
    ORDER BY created_at DESC 
    LIMIT ?
    ''', (user_id, limit))
    recent_data = c.fetchall()
    conn.close()
    return recent_data

# Inisialisasi database
init_database()

# Inisialisasi session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'show_register' not in st.session_state:
    st.session_state.show_register = False
if 'show_delete_confirmation' not in st.session_state:
    st.session_state.show_delete_confirmation = False
if 'delete_all_confirmation' not in st.session_state:
    st.session_state.delete_all_confirmation = False
if 'prediction_made' not in st.session_state:
    st.session_state.prediction_made = False
if 'last_prediction_result' not in st.session_state:
    st.session_state.last_prediction_result = None


# Halaman Login/Register
if not st.session_state.logged_in:
    # Header
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">🏥 Sistem Deteksi Dini Stunting</h1>
        <p class="subtitle">Platform untuk Petugas Kesehatan</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.show_register:
            # Form Login
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### 🔐 Login Petugas Kesehatan")
            
            with st.form("login_form"):
                username = st.text_input("👤 Username", placeholder="Masukkan username Anda")
                password = st.text_input("🔒 Password", type="password", placeholder="Masukkan password Anda")
                
                col_login, col_register = st.columns(2)
                with col_login:
                    login_button = st.form_submit_button("Login", use_container_width=True)
                with col_register:
                    register_button = st.form_submit_button("Register", use_container_width=True)
                
                if login_button:
                    if username and password:
                        user = login_user(username, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_info = user
                            st.success(f"Selamat datang, {user['nama_lengkap']}!")
                            st.rerun()
                        else:
                            st.error("❌ Username atau password salah!")
                    else:
                        st.warning("❗Mohon lengkapi semua field!")
                
                if register_button:
                    st.session_state.show_register = True
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
        else:
            # Form Register
            st.markdown('<div class="form-container">', unsafe_allow_html=True)
            st.markdown("### 📝 Registrasi Petugas Kesehatan Baru")
            
            with st.form("register_form"):
                reg_username = st.text_input("👤 Username", placeholder="Pilih username unik")
                reg_password = st.text_input("🔒 Password", type="password", placeholder="Buat password yang kuat")
                reg_confirm_password = st.text_input("🔒 Konfirmasi Password", type="password", placeholder="Ulangi password")
                reg_nama_lengkap = st.text_input("👨‍⚕️ Nama Lengkap", placeholder="Masukkan nama lengkap")
                reg_jabatan = st.selectbox("💼 Jabatan", 
                                    options=["Dokter", "Perawat", "Bidan", "Ahli Gizi", "Tenaga Kesehatan Masyarakat", "Lainnya"],
                                    index=None, placeholder="Pilih Jabatan Anda")
                reg_instansi = st.text_input("🏥 Instansi", placeholder="Puskesmas/Rumah Sakit/Klinik")
                
                col_back, col_submit = st.columns(2)
                with col_back:
                    back_button = st.form_submit_button("⬅️ Kembali", use_container_width=True)
                with col_submit:
                    submit_button = st.form_submit_button("✅ Register", use_container_width=True)
                
                if back_button:
                    st.session_state.show_register = False
                    st.rerun()
                
                if submit_button:
                    if all([reg_username, reg_password, reg_confirm_password, reg_nama_lengkap, reg_instansi]):
                        if reg_password == reg_confirm_password:
                            if len(reg_password) >= 6:
                                if register_user(reg_username, reg_password, reg_nama_lengkap, reg_jabatan, reg_instansi):
                                    st.success("✅ Registrasi berhasil! Silakan login.")
                                    st.session_state.show_register = False
                                    st.rerun()
                                else:
                                    st.error("❌ Username sudah digunakan!")
                            else:
                                st.error("❌ Password minimal 6 karakter!")
                        else:
                            st.error("❌ Konfirmasi password tidak cocok!")
                    else:
                        st.warning("❗ Mohon lengkapi semua field!")
            
            st.markdown('</div>', unsafe_allow_html=True)

else:
    # Halaman utama setelah login
    user_info = st.session_state.user_info
    
    # Header dengan info user
    col_header1, col_header2, col_header3 = st.columns([2, 1, 1])
    
    with col_header1:
        st.markdown(f"""
        <div class="user-info">
            <h2>👋 Selamat datang, {user_info['nama_lengkap']}</h2>
            <p>{user_info['jabatan']} - {user_info['instansi']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_header3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_info = None
            st.session_state.prediction_made = False
            st.session_state.last_prediction_result = None
            st.rerun()
    
    # Load model dan scaler
    try:
        classifier = pickle.load(open('stunting.sav', 'rb'))
        scaler = pickle.load(open('scaler.sav', 'rb'))
    except FileNotFoundError:
        st.error("❌ File model tidak ditemukan! Pastikan file 'stunting.sav' dan 'scaler.sav' tersedia.")
        st.stop()
    
    # Sidebar dengan statistik dan riwayat
    with st.sidebar:
        st.markdown("### 📊 Statistik Anda")
        
        stats = get_user_statistics(user_info['id'])
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{stats['total_prediksi']}</div>
            <div class="stat-label">Total Prediksi</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #ff4757;">{stats['berisiko']}</div>
            <div class="stat-label">Berisiko Stunting</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number" style="color: #2ed573;">{stats['tidak_berisiko']}</div>
            <div class="stat-label">Tidak Berisiko</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Riwayat prediksi
        st.markdown("### 📋 Riwayat Prediksi")
        
        recent_data = get_recent_predictions(user_info['id'], 5)
        
        if recent_data:
            for data in recent_data:
                icon = "🔴" if data[1] == "Berisiko stunting" else "🟢"
                date_str = data[2][:10] if data[2] else "N/A"
                st.markdown(f"{icon} **{data[0]}** - {date_str}")
        else:
            st.info("Belum ada riwayat prediksi")
        
        col_history, col_delete = st.columns(2)
        with col_history:
            if st.button("📊 Lihat Semua"):
                st.session_state.show_history = True
        
        with col_delete:
            if stats['total_prediksi'] > 0:
                if st.button("🗑️ Hapus Semua"):
                    st.session_state.delete_all_confirmation = True
    
    # Main content
    st.markdown("""
    <div class="header-container">
        <h1 class="main-title">👶 Deteksi Risiko Stunting</h1>
        <p class="subtitle">Masukkan data anak untuk analisis risiko stunting</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Konfirmasi hapus semua riwayat
    if st.session_state.delete_all_confirmation:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.warning("⚠️ **Konfirmasi Hapus Semua Riwayat**")
        st.write("Apakah Anda yakin ingin menghapus semua riwayat prediksi? Tindakan ini tidak dapat dibatalkan.")
        
        col_cancel, col_confirm = st.columns(2)
        with col_cancel:
            if st.button("❌ Batal", use_container_width=True):
                st.session_state.delete_all_confirmation = False
                st.rerun()
        
        with col_confirm:
            if st.button("✅ Ya, Hapus Semua", use_container_width=True):
                deleted_count = delete_all_predictions(user_info['id'])
                if deleted_count > 0:
                    st.success(f"✅ Berhasil menghapus {deleted_count} riwayat prediksi.")
                else:
                    st.info("ℹ️ Tidak ada riwayat yang dihapus.")
                st.session_state.delete_all_confirmation = False
                st.session_state.show_history = False
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Form input dalam card
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # Tampilkan hasil prediksi jika ada
        if st.session_state.prediction_made and st.session_state.last_prediction_result:
            result = st.session_state.last_prediction_result
            
            st.markdown("### 📊 Hasil Analisis")

            # HASIL PREDIKSI TANPA FADE (HTML, BUKAN st.success/st.error)
            if result['prediksi'] == 1:
                st.markdown(
                    f"""
                    <div class="result-alert result-alert-risk">
                        ⚠️ <strong>{result['Nama']} berisiko mengalami stunting</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("""
                **🏥 Rekomendasi Tindakan:**
                - Pemberian Makanan Tambahan 
                - Monitoring atau tumbuh kembang anak
                - Membawa ke posyandu secara berkala
                - Edukasi orangtua tentang gizi seimbang
                """)
            else:
                st.markdown(
                    f"""
                    <div class="result-alert result-alert-safe">
                        ✅ <strong>{result['Nama']} tidak berisiko stunting</strong>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown("""
                **💡 Tips Pemeliharaan:**
                - Lanjutkan pola pemberian makan yang baik
                - Pantau pertumbuhan secara berkala
                - Pastikan imunisasi lengkap sesuai jadwal
                - Edukasi orangtua tentang deteksi dini masalah pertumbuhan
                """)

            
            # Tampilkan ringkasan data
            st.markdown("---")
            st.markdown("### 📋 Ringkasan Data Anak")
            
            data_summary = pd.DataFrame({
                'Parameter': ['Nama Anak', 'Nama Ayah', 'Nama Ibu', 'Jenis Kelamin', 'Usia (bulan)', 'Berat Badan Lahir (kg)', 
                            'Tingggi Badan Lahir (cm)', 'Berat Berat Sekarang (kg)', 'Tinggi Badan Sekarang (cm)'],
                'Nilai': [str(result['Nama']), str(result['Nama_Ayah']), str(result['Nama_Ibu']), str(result['Jenis_Kelamin']), str(result['Usia']), str(result['BB_Lahir']), 
                         str(result['TB_Lahir']), str(result['BB_Sekarang']), str(result['TB_Sekarang'])]
            })
            
            st.table(data_summary.set_index('Parameter'))
            
            # Tombol untuk membuat prediksi baru
            if st.button("🔄 Analisis Baru", use_container_width=True):
                st.session_state.prediction_made = False
                st.session_state.last_prediction_result = None
                st.rerun()
            
            st.markdown("---")
        
        # Form input prediksi
        if not st.session_state.prediction_made:
            with st.form("prediction_form"):
                st.markdown("### 📝 Data Anak")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    nama = st.text_input("👶 Nama Anak", placeholder="Masukkan nama lengkap anak")
                    nama_ayah = st.text_input("Nama Ayah", placeholder="Masukkan Nama Ayah")
                    nama_ibu = st.text_input("Nama Ibu", placeholder="Masukkan Nama Ibu")
                    gender = st.selectbox("🚻 Jenis Kelamin", ["Laki-laki", "Perempuan"])
                    usia = st.number_input("🕒 Usia (bulan)", placeholder= "Masukkan Usia Anak",min_value=0, max_value=60, step=1, value=None)
                
                with col2:
                    bb_lahir = st.number_input("⚖️ Berat Badan Lahir (kg)", placeholder= "Masukkan Berat Badan Lahir Anak", min_value=1.0, max_value=5.0, step=0.1, value=None)
                    tb_lahir = st.number_input("📏 Tinggi Badan Lahir (cm)", placeholder= "Masukkan Tinggi Badan Lahir Anak", min_value=30.0, max_value=60.0, step=0.1, value=None)
                    bb_sekarang = st.number_input("⚖️ Berat Badan Sekarang (kg)", placeholder= "Masukkan Berat Badan Saat Pemeriksaan",min_value=1.0, max_value=20.0, step=0.1, value=None)
                    tb_sekarang = st.number_input("📏 Tinggi Badan Sekarang (cm)", placeholder= "Masukkan Tinggi Badan Saat Pemeriksaan", min_value=30.0, max_value=120.0, step=0.1, value=None)
                    
                
                submitted = st.form_submit_button("🔍 Analisis Risiko Stunting", use_container_width=True)
                
                if submitted:
                    if nama.strip() and nama_ayah.strip() and nama_ibu.strip():
                        # Konversi input ke format yang sesuai
                        gender_num = 0 if gender == "Perempuan" else 1
                       
                        
                        # Membuat array input
                        input_data = (gender_num, usia, bb_lahir, tb_lahir, 
                                    bb_sekarang, tb_sekarang)
                        
                        input_data_as_numpy_array = np.array(input_data).reshape(1, -1)
                        
                        # Normalisasi data input
                        std_data = scaler.transform(input_data_as_numpy_array)
                        
                        # Prediksi
                        prediction = classifier.predict(std_data)
                        
                        # Menyimpan hasil prediksi
                        hasil_prediksi = "Berisiko stunting" if prediction[0] == 1 else "Tidak berisiko stunting"
                        
                        # Simpan ke database
                        conn = sqlite3.connect('stunting_app.db')
                        c = conn.cursor()
                        c.execute('''
                        INSERT INTO prediksi_stunting 
                        (user_id, Nama, Nama_Ayah, Nama_Ibu, Jenis_Kelamin, Usia, BB_Lahir, TB_Lahir, 
                         BB_Sekarang, TB_Sekarang, hasil_prediksi) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (user_info['id'], nama, nama_ayah, nama_ibu, gender, usia, bb_lahir, tb_lahir, 
                              bb_sekarang, tb_sekarang, hasil_prediksi))
                        conn.commit()
                        conn.close()
                        
                        # Simpan hasil ke session state
                        st.session_state.prediction_made = True
                        st.session_state.last_prediction_result = {
                            'Nama': nama,
                            'Nama_Ayah': nama_ayah,
                            'Nama_Ibu' : nama_ibu,
                            'Jenis_Kelamin': gender,
                            'Usia': usia,
                            'BB_Lahir': bb_lahir,
                            'TB_Lahir': tb_lahir,
                            'BB_Sekarang': bb_sekarang,
                            'TB_Sekarang': tb_sekarang,
                            'prediksi': prediction[0]
                        }
                        
                        # Rerun untuk memperbarui tampilan
                        st.rerun()
                        
                    else:
                        st.warning("⚠️ Mohon periksa nama anak dan nama orang tua untuk melanjutkan analisis.")
                            
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ================= RIWAYAT LENGKAP =================
if 'show_history' in st.session_state and st.session_state.show_history:
    st.markdown("---")
    st.markdown("### 📊 Riwayat Lengkap Prediksi")

    # ===== AMBIL DATA DARI DATABASE =====
    conn = sqlite3.connect('stunting_app.db')
    df_history = pd.read_sql_query('''
        SELECT Nama, Nama_Ayah, Nama_Ibu, Jenis_Kelamin, Usia,
               BB_Lahir, TB_Lahir, BB_Sekarang, TB_Sekarang,
               hasil_prediksi, created_at
        FROM prediksi_stunting
        WHERE user_id = ?
        ORDER BY created_at DESC
    ''', conn, params=(user_info['id'],))
    conn.close()

    if not df_history.empty:

        # ===== FORMAT DATA =====
        df_history['created_at'] = pd.to_datetime(df_history['created_at']).dt.strftime('%Y-%m-%d')

        df_history.columns = [
            'Nama', 'Nama Ayah', 'Nama Ibu', 'Jenis Kelamin',
            'Usia (bln)', 'BB Lahir (kg)', 'TB Lahir (cm)',
            'BB Sekarang (kg)', 'TB Sekarang (cm)',
            'Hasil Prediksi', 'Tanggal Periksa'
        ]

        # Ubah semua ke string agar aman difilter
        for col in df_history.columns:
            df_history[col] = df_history[col].astype(str)

        # ===== FILTER =====
        
        col_left, col_filter = st.columns([7, 3])
        with col_filter :
            global_filter = st.text_input(
            " ",
            placeholder="Cari Data Anak"
        )
    
        if global_filter:
            keyword = global_filter.lower()

            df_history = df_history[
                df_history.apply(
                    lambda row: keyword in ' '.join([
                        row['Nama'].lower(),
                        row['Nama Ayah'].lower(),
                        row['Nama Ibu'].lower(),
                        row['Jenis Kelamin'].lower(),
                        row['Usia (bln)'].lower(),
                        row['Hasil Prediksi'].lower()
                    ]),
                    axis=1
                )
            ]

        # ===== TAMPILKAN DATA =====
        if df_history.empty:
            st.warning("❗ Data Tidak Ditemukan.")
        else:
            st.dataframe(df_history, use_container_width=True)

            # ===== DOWNLOAD =====
            col_csv, col_excel = st.columns(2)
            today = datetime.now().strftime("%Y-%m-%d")

            with col_csv:
                csv_data = df_history.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"riwayat_deteksi_stunting_{today}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

            with col_excel:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer) as writer:
                    df_history.to_excel(writer, index=False, sheet_name="Riwayat Prediksi")

                st.download_button(
                    label="📥 Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"riwayat_deteksi_stunting_{today}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

            # ===== TOMBOL AKSI =====
            col_close, col_delete_all = st.columns(2)

            with col_close:
                if st.button("❌ Tutup Riwayat", use_container_width=True):
                    st.session_state.show_history = False
                    st.rerun()

            with col_delete_all:
                if st.button("🗑️ Hapus Semua Riwayat", use_container_width=True):
                    st.session_state.delete_all_confirmation = True
                    st.session_state.show_history = False
                    st.rerun()

    else:
        st.info("Belum ada riwayat prediksi.")
        if st.button("❌ Tutup Riwayat"):
            st.session_state.show_history = False
            st.rerun()



# Cara Running
# py -m streamlit run web_deteksi_stunting.py