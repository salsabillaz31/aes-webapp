import streamlit as st
import pandas as pd
from config.db_config import get_connection
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# =============== HIDE DEFAULT SIDEBAR NAVIGATION ===============
hide_nav_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_nav_style, unsafe_allow_html=True)

# =============== KONFIGURASI HALAMAN ===============
st.set_page_config(
    page_title="Dashboard Dosen",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============== ENHANCED CSS UNTUK SOFT INTERACTIVE THEME ===============
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
    .main { 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .stApp { 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
        color: black !important;
    }
    
    
    /* Header dengan glassmorphism effect */
    .header-container {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: #2d3748;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb, #f5576c);
        animation: gradient-animation 3s ease infinite;
    }
    
    @keyframes gradient-animation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Metric cards dengan hover effects */
    .metric-card {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        background: rgba(255, 255, 255, 0.9);
    }
    
    .metric-card .metric-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2d3748;
        margin: 0.5rem 0;
    }
    
    .metric-card .metric-label {
        color: #718096;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    /* Section headers dengan underline animation */
    .section-header {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.4rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        position: relative;
        display: inline-block;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0;
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 2px;
        animation: underline-expand 1s ease-out forwards;
    }
    
    @keyframes underline-expand {
        to { width: 100%; }
    }
    
    /* Form containers dengan soft shadows */
    .form-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .form-container:hover {
        box-shadow: 0 6px 35px rgba(0,0,0,0.15);
    }
    
    /* Info boxes dengan soft colors */
    .info-box {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(8px);
        color: #4a5568;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 15px rgba(0,0,0,0.1);
    }
    
    .success-box {
        background: rgba(72, 187, 120, 0.1);
        backdrop-filter: blur(8px);
        color: #2f855a;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #48bb78;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: rgba(237, 137, 54, 0.1);
        backdrop-filter: blur(8px);
        color: #c05621;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ed8936;
        margin: 1rem 0;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #5a67d8, #6b46c1);
    }
    
    /* Stats container */
    .stats-container {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    
    /* Chart container */
    .chart-container {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
            
    /* Kurangi jarak antara label dan multiselect */
    .custom-label {
        margin-bottom: -150px;
        font-weight: 600;
        font-size: 16px;
        color: #264653;
    }

    /* Gaya untuk multiselect */
    div[data-baseweb="select"] {
        background-color: white;     /* Ganti warna latar */
        color: white;                /* Warna teks */
        border: 1px solid black;     /* Warna border */
        border-radius: 10px;           /* Sudut melengkung */
        padding: 4px;
    }
            
    /* Dropdown saat terbuka */
    div[data-baseweb="popover"] {
        background-color: #e8eb1d !important;
    }
            
    .section-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #264653; /* Ganti warna sesuai tema */
    margin-top: 2rem;
    margin-bottom: 1rem;
    position: relative;
    display: inline-block;
    }

    .section-title::after {
        content: '';
        display: block;
        width: 0;
        height: 3px;
        background: linear-gradient(90deg, #f093fb, #f5576c);  /* Gradasi pink-merah */
        animation: underline-expand 1s ease-out forwards;
        border-radius: 2px;
        margin-top: 5px;
    }

    @keyframes underline-expand {
        to { width: 100%; }
    }
            
    /* Paksa color-scheme agar light */
    html, body, [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
    }

    /* Gaya label radio */
    div[data-testid="stRadio"] div[role="radiogroup"] > label > div {
        color: #e76f51 !important;  /* Warna tulisan */
        font-weight: bold !important;
        font-size: 15px !important;
    }
            
    .custom-table {
    width: 100%;
    border-collapse: collapse;
    background-color: #fff3f7;
    color: black;
    }

    .custom-table th {
    background-color: #eb1d67;
    color: white;
    padding: 8px;
    }

    .custom-table td {
    padding: 8px;
    text-align: center;
    border: 1px solid #ddd;
    }

    .custom-table tr:hover {
    background-color: #ffd9e6;
    }
            
    /* Ubah warna tulisan tombol download */
    button[data-testid="baseButton-download"] {
        color: white !important;          /* warna tulisan */
        background-color: #eb1d67 !important; /* warna latar belakang tombol */
        border: none;
    }

    button[data-testid="baseButton-download"]:hover {
        background-color: #c01757 !important; /* warna saat hover */
    }
            
    div:has(> button:contains('Download Rekap Detail')) button {
    color: white !important;
    background-color: #f2e4e9 !important;
    }
     
</style>

""", unsafe_allow_html=True)

# =============== SIDEBAR ===============
st.sidebar.markdown("## 🎓 Dashboard Dosen")
st.sidebar.markdown("---")

kompetensi_options = ["Machine Learning", "Data Mining", "Neuro Computing"]
selected_kompetensi = st.sidebar.selectbox(
    "🎯 Pilih Kompetensi",
    kompetensi_options,
    key="kompetensi_selector"
)

st.sidebar.markdown("---")
menu_option = st.sidebar.radio(
    "📊 Navigasi",
    ["📝 Manajemen Ujian", "📊 Nilai Mahasiswa", "📈 Rekap Detail"],
    key="menu_navigation"
)

# Tombol Logout di sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("✅ Berhasil logout. Mengalihkan ke halaman login...")
    st.switch_page("pages/login.py")

# =============== CEK SESSION DAN ROLE ===============
if "role" not in st.session_state:
    st.switch_page("pages/login.py")
elif st.session_state["role"] != "dosen":
    st.error("❌ Anda tidak punya akses ke halaman ini.")
    st.stop()

# =============== HEADER ===============
st.markdown(f"""
<div class="header-container">
    <h1 style="margin: 0; font-size: 2.5rem; font-weight: 700;">🎓 Dashboard Dosen</h1>
    <p style="margin: 0.5rem 0; font-size: 1.1rem; opacity: 0.8;">Selamat datang, <strong>{st.session_state.get('username', 'Dosen')}</strong>!</p>
    <p style="margin: 0; font-size: 1rem; opacity: 0.7;">Kompetensi Aktif: <strong>{selected_kompetensi}</strong></p>
</div>
""", unsafe_allow_html=True)

# =============== KONEKSI DB ===============
conn = get_connection()
cur = conn.cursor()

# =============== STATISTIK DASHBOARD ===============
col1, col2, col3, col4 = st.columns(4)

cur.execute("SELECT COUNT(*) FROM list_soal WHERE kompetensi = %s", (selected_kompetensi,))
total_soal = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM nama_ujian WHERE kompetensi = %s", (selected_kompetensi,))
total_ujian = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM nama_ujian WHERE kompetensi = %s AND aktif = TRUE", (selected_kompetensi,))
ujian_aktif_count = cur.fetchone()[0]

cur.execute("""
    SELECT COUNT(DISTINCT jm.username)
    FROM jawaban_mahasiswa jm
    JOIN nama_ujian nu ON jm.id_ujian = nu.id_ujian
    WHERE nu.kompetensi = %s
""", (selected_kompetensi,))
total_mahasiswa = cur.fetchone()[0]

metrics_data = [
    ("📚", "Total Soal", total_soal),
    ("📝", "Total Ujian", total_ujian),
    ("🟢", "Ujian Aktif", ujian_aktif_count),
    ("👥", "Total Mahasiswa", total_mahasiswa)
]

for col, (icon, label, val) in zip([col1, col2, col3, col4], metrics_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

# =============== KONTEN MENU =============== 
# =============== KONTEN MENU - MANAJEMEN UJIAN =============== 
if menu_option == "📝 Manajemen Ujian":
    
    # ===== SECTION 1: PILIH SOAL =====
    cur.execute("SELECT id_question, pertanyaan FROM list_soal WHERE kompetensi = %s", (selected_kompetensi,))
    soal_list = cur.fetchall()

    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 30px; border-radius: 20px; margin: 20px 0; 
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
                border: 2px solid rgba(255,255,255,0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background: rgba(255,255,255,0.2); border-radius: 50%; 
                        width: 50px; height: 50px; display: flex; align-items: center; 
                        justify-content: center; margin-right: 15px;">
                <span style="font-size: 24px;">📋</span>
            </div>
            <h2 style="color: white; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                Pilih Soal untuk Ujian
            </h2>
        </div>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px; line-height: 1.6;">
            Pilih soal-soal yang akan digunakan dalam ujian dari bank soal kompetensi <strong>{selected_kompetensi}</strong>
        </p>
    </div>
    """.format(selected_kompetensi=selected_kompetensi), unsafe_allow_html=True)

    if soal_list:
        # Info Box tentang soal yang tersedia
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); 
                    border-left: 6px solid #28a745; padding: 20px; border-radius: 12px; 
                    margin: 20px 0; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 15px;">✅</span>
                <div>
                    <h4 style="color: #155724; margin: 0; font-size: 18px; font-weight: 600;">
                        Bank Soal Tersedia
                    </h4>
                    <p style="color: #155724; margin: 5px 0 0 0; font-size: 16px;">
                        Terdapat <strong>{len(soal_list)} soal</strong> yang dapat dipilih untuk ujian kompetensi {selected_kompetensi}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Judul manual dengan margin kecil
        st.markdown('<p class="custom-label">🎯 Daftar Soal yang Tersedia:</p>', unsafe_allow_html=True)

        # Multiselect tetap dengan semua parameter
        selected_soal = st.multiselect(
            label="",
            options=soal_list,
            format_func=lambda x: f"📄 ID: {x[0]} - {x[1][:120]}{'...' if len(x[1]) > 120 else ''}",
            key="soal_multiselect",
            help=f"Pilih satu atau lebih soal dari {len(soal_list)} soal yang tersedia"
        )
        
        if selected_soal:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #cce5ff 0%, #b3d9ff 100%); 
                        border-left: 6px solid #007bff; padding: 20px; border-radius: 12px; 
                        margin: 15px 0; box-shadow: 0 4px 15px rgba(0, 123, 255, 0.2);">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 24px; margin-right: 15px;">🎯</span>
                    <div>
                        <h4 style="color: #004085; margin: 0; font-size: 18px; font-weight: 600;">
                            Soal Terpilih
                        </h4>
                        <p style="color: #004085; margin: 5px 0 0 0; font-size: 16px;">
                            <strong>{len(selected_soal)} soal</strong> telah dipilih dan siap digunakan untuk ujian
                        </p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                    border-left: 6px solid #ffc107; padding: 25px; border-radius: 12px; 
                    margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 28px; margin-right: 15px;">⚠️</span>
                <div>
                    <h4 style="color: #856404; margin: 0; font-size: 20px; font-weight: 600;">
                        Bank Soal Kosong
                    </h4>
                    <p style="color: #856404; margin: 8px 0 0 0; font-size: 16px; line-height: 1.5;">
                        Tidak ada soal tersedia untuk kompetensi ini. Silakan tambahkan soal terlebih dahulu 
                        sebelum membuat ujian.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        selected_soal = []

    # ===== SECTION 2: BUAT UJIAN BARU =====
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                padding: 30px; border-radius: 20px; margin: 60px 0 -50px 0; 
                box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
                border: 2px solid rgba(255,255,255,0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background: rgba(255,255,255,0.2); border-radius: 50%; 
                        width: 50px; height: 50px; display: flex; align-items: center; 
                        justify-content: center; margin-right: 15px;">
                <span style="font-size: 24px;">📝</span>
            </div>
            <h2 style="color: white; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                Buat Ujian Baru
            </h2>
        </div>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px; line-height: 1.6;">
            Buat ujian baru dengan menggunakan soal-soal yang telah dipilih dari kompetensi <strong>{selected_kompetensi}</strong>
        </p>
    </div>
    """.format(selected_kompetensi=selected_kompetensi), unsafe_allow_html=True)

    with st.form("form_ujian"):
        st.markdown('<div class="section-title">📋 Detail Ujian</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="custom-label">🏷️ Nama Ujian</div>', unsafe_allow_html=True)
            nama_ujian = st.text_input(
                label="", 
                placeholder="Contoh: Ujian Tengah Semester Machine Learning",
                help="Masukkan nama ujian yang jelas dan deskriptif"
            )
        
        with col2:
            st.markdown('<div class="custom-label">📅 Tanggal Pelaksanaan</div>', unsafe_allow_html=True)
            tanggal_mulai = st.date_input(
                label = "", 
                help="Pilih tanggal ujian akan dilaksanakan"
            )
        
        # Preview section
        if selected_soal:
            st.markdown("### 📊 Preview Ujian")
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9ff 0%, #e6f3ff 100%); 
                        padding: 20px; border-radius: 15px; margin: 15px 0; 
                        border: 2px solid #e3f2fd; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="text-align: center;">
                        <div style="background: #2196f3; color: white; border-radius: 50%; 
                                   width: 40px; height: 40px; display: flex; align-items: center; 
                                   justify-content: center; margin: 0 auto 10px; font-size: 18px; font-weight: bold;">
                            {len(selected_soal)}
                        </div>
                        <p style="margin: 0; color: #1976d2; font-weight: 600; font-size: 14px;">Jumlah Soal</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #4caf50; color: white; border-radius: 50%; 
                                   width: 40px; height: 40px; display: flex; align-items: center; 
                                   justify-content: center; margin: 0 auto 10px; font-size: 18px; font-weight: bold;">
                            {len(selected_soal) * 5}
                        </div>
                        <p style="margin: 0; color: #388e3c; font-weight: 600; font-size: 14px;">Total Poin</p>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: #ff9800; color: white; border-radius: 50%; 
                                   width: 40px; height: 40px; display: flex; align-items: center; 
                                   justify-content: center; margin: 0 auto 10px; font-size: 14px; font-weight: bold;">
                            ~{len(selected_soal) * 2}
                        </div>
                        <p style="margin: 0; color: #f57c00; font-weight: 600; font-size: 14px;">Estimasi Menit</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Submit section
        st.markdown('<div class="section-title">🚀 Finalisasi Ujian</div>', unsafe_allow_html=True)

        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if selected_soal:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); 
                            padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <p style="color: #155724; margin: 0; font-size: 16px; font-weight: 500;">
                        ✅ Siap membuat ujian dengan <strong>{len(selected_soal)} soal</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                            padding: 15px; border-radius: 10px; margin: 10px 0;">
                    <p style="color: #721c24; margin: 0; font-size: 16px; font-weight: 500;">
                        ❌ Pilih minimal 1 soal untuk membuat ujian
                    </p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            submitted = st.form_submit_button(
                "🚀 Buat Ujian", 
                use_container_width=True,
                disabled=not selected_soal,
                type="primary"
            )

        if submitted:
            if nama_ujian and selected_soal and tanggal_mulai:
                try:
                    cur.execute("""
                        INSERT INTO nama_ujian (nama_ujian, tanggal_mulai, aktif, kompetensi)
                        VALUES (%s, %s, TRUE, %s)
                        RETURNING id_ujian
                    """, (nama_ujian, tanggal_mulai, selected_kompetensi))
                    id_ujian_baru = cur.fetchone()[0]

                    for soal in selected_soal:
                        cur.execute("""
                            INSERT INTO soal_ujian (id_ujian, id_question)
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING
                        """, (id_ujian_baru, soal[0]))

                    conn.commit()
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                border-left: 6px solid #28a745; padding: 25px; border-radius: 12px; 
                                margin: 20px 0; box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 32px; margin-right: 20px;">🎉</span>
                            <div>
                                <h3 style="color: #155724; margin: 0; font-size: 22px; font-weight: 700;">
                                    Ujian Berhasil Dibuat!
                                </h3>
                                <p style="color: #155724; margin: 8px 0 5px 0; font-size: 16px; line-height: 1.5;">
                                    <strong>"{nama_ujian}"</strong> telah dibuat dengan <strong>{len(selected_soal)} soal</strong>
                                </p>
                                <p style="color: #155724; margin: 0; font-size: 14px;">
                                    📅 Tanggal pelaksanaan: <strong>{tanggal_mulai.strftime("%d %B %Y")}</strong>
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                                border-left: 6px solid #dc3545; padding: 20px; border-radius: 12px; 
                                margin: 20px 0; box-shadow: 0 6px 20px rgba(220, 53, 69, 0.3);">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 28px; margin-right: 15px;">❌</span>
                            <div>
                                <h4 style="color: #721c24; margin: 0; font-size: 18px; font-weight: 600;">
                                    Gagal Membuat Ujian
                                </h4>
                                <p style="color: #721c24; margin: 5px 0 0 0; font-size: 14px;">
                                    Terjadi kesalahan saat menyimpan data ujian.
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%); 
                            border-left: 6px solid #ffc107; padding: 20px; border-radius: 12px; 
                            margin: 20px 0; box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);">
                    <div style="display: flex; align-items: center;">
                        <span style="font-size: 28px; margin-right: 15px;">⚠️</span>
                        <div>
                            <h4 style="color: #856404; margin: 0; font-size: 18px; font-weight: 600;">
                                Data Tidak Lengkap
                            </h4>
                            <p style="color: #856404; margin: 5px 0 0 0; font-size: 16px;">
                                Mohon lengkapi nama ujian, tanggal pelaksanaan, dan pilih minimal 1 soal!
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ===== SECTION 3: TANDAI UJIAN SELESAI =====
    st.markdown("""
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                padding: 30px; border-radius: 20px; margin: 60px 0 0px 0; 
                box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
                border: 2px solid rgba(255,255,255,0.2);">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <div style="background: rgba(255,255,255,0.2); border-radius: 50%; 
                        width: 50px; height: 50px; display: flex; align-items: center; 
                        justify-content: center; margin-right: 15px;">
                <span style="font-size: 24px;">🔒</span>
            </div>
            <h2 style="color: white; margin: 0; font-size: 28px; font-weight: 700; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                Tandai Ujian Selesai
            </h2>
        </div>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 16px; line-height: 1.6;">
            Tutup ujian yang sudah selesai dan hitung nilai akhir mahasiswa secara otomatis
        </p>
    </div>
    """, unsafe_allow_html=True)

    cur.execute("""
        SELECT id_ujian, nama_ujian, tanggal_mulai
        FROM nama_ujian
        WHERE aktif = TRUE AND kompetensi = %s
        ORDER BY tanggal_mulai DESC
    """, (selected_kompetensi,))
    ujian_aktif = cur.fetchall()

    if ujian_aktif:
        # Info tentang ujian aktif
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%); 
                    border-left: 6px solid #28a745; padding: 20px; border-radius: 12px; 
                    margin: 20px 0; box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 24px; margin-right: 15px;">🟢</span>
                <div>
                    <h4 style="color: #155724; margin: 0; font-size: 18px; font-weight: 600;">
                        Ujian Aktif Tersedia
                    </h4>
                    <p style="color: #155724; margin: 5px 0 0 0; font-size: 16px;">
                        Terdapat <strong>{len(ujian_aktif)} ujian aktif</strong> yang dapat ditutup untuk kompetensi {selected_kompetensi}
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown('<div class="custom-label">🎯 Pilih Ujian yang Akan Ditutup:</div>', unsafe_allow_html=True)
            selected_selesai = st.selectbox(
                "",
                ujian_aktif,
                format_func=lambda x: f"📝 {x[1]} (📅 {x[2].strftime('%d %B %Y')})",
                key="ujian_selesai_select",
                help="Pilih ujian yang akan ditandai selesai dan dihitung nilai akhirnya"
            )

        with col2:
            if st.button("🔒 Tutup Ujian", key="tandai_selesai_btn", use_container_width=True, type="primary"):
                try:
                    # Update status ujian
                    cur.execute("UPDATE nama_ujian SET aktif = FALSE WHERE id_ujian = %s", (selected_selesai[0],))

                    # Hitung dan simpan nilai akhir
                    cur.execute("""
                        SELECT username, COUNT(*), SUM(skor_final)
                        FROM jawaban_mahasiswa
                        WHERE id_ujian = %s
                        GROUP BY username
                    """, (selected_selesai[0],))
                    nilai_akhir = cur.fetchall()

                    for username, total_soal, total_nilai in nilai_akhir:
                        nilai_akhir_persen = round((total_nilai / (total_soal * 5)) * 100)
                        cur.execute("""
                            INSERT INTO nilai_akhir_mahasiswa (username, id_ujian, nilai_akhir)
                            VALUES (%s, %s, %s)
                            ON CONFLICT (username, id_ujian) DO UPDATE
                            SET nilai_akhir = EXCLUDED.nilai_akhir
                        """, (username, selected_selesai[0], nilai_akhir_persen))

                    conn.commit()
                    
                    # Refresh session state
                    st.session_state["role"] = "dosen"
                    st.session_state["username"] = st.session_state.get("username", "dosen")
                    
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%); 
                                border-left: 6px solid #28a745; padding: 25px; border-radius: 12px; 
                                margin: 20px 0; box-shadow: 0 6px 20px rgba(40, 167, 69, 0.3);">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 32px; margin-right: 20px;">✅</span>
                            <div>
                                <h3 style="color: #155724; margin: 0; font-size: 22px; font-weight: 700;">
                                    Ujian Berhasil Ditutup!
                                </h3>
                                <p style="color: #155724; margin: 8px 0 5px 0; font-size: 16px; line-height: 1.5;">
                                    <strong>"{selected_selesai[1]}"</strong> telah ditutup dan nilai akhir mahasiswa telah dihitung
                                </p>
                                <p style="color: #155724; margin: 0; font-size: 14px;">
                                    📅 Ujian tanggal: <strong>{selected_selesai[2].strftime("%d %B %Y")}</strong>
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.rerun()
                    
                except Exception as e:
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
                                border-left: 6px solid #dc3545; padding: 20px; border-radius: 12px; 
                                margin: 20px 0; box-shadow: 0 6px 20px rgba(220, 53, 69, 0.3);">
                        <div style="display: flex; align-items: center;">
                            <span style="font-size: 28px; margin-right: 15px;">❌</span>
                            <div>
                                <h4 style="color: #721c24; margin: 0; font-size: 18px; font-weight: 600;">
                                    Gagal Menutup Ujian
                                </h4>
                                <p style="color: #721c24; margin: 5px 0 0 0; font-size: 14px;">
                                    Terjadi kesalahan saat memproses penutupan ujian.
                                </p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    border-left: 6px solid #2196f3; padding: 25px; border-radius: 12px; 
                    margin: 20px 0; box-shadow: 0 4px 15px rgba(33, 150, 243, 0.2);">
            <div style="display: flex; align-items: center;">
                <span style="font-size: 28px; margin-right: 15px;">ℹ️</span>
                <div>
                    <h4 style="color: #0d47a1; margin: 0; font-size: 20px; font-weight: 600;">
                        Tidak Ada Ujian Aktif
                    </h4>
                    <p style="color: #0d47a1; margin: 8px 0 0 0; font-size: 16px; line-height: 1.5;">
                        Saat ini tidak ada ujian aktif untuk kompetensi <strong>{selected_kompetensi}</strong>. 
                        Buat ujian baru terlebih dahulu di bagian atas.
                    </p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif menu_option == "📊 Nilai Mahasiswa":
    st.markdown('<div class="section-header">🏁 Nilai Akhir Mahasiswa</div>', unsafe_allow_html=True)

    # Filter Controls dengan container yang benar
    col1, col2 = st.columns(2)

    with col1:
        cur.execute("SELECT DISTINCT nama_ujian FROM nama_ujian WHERE kompetensi = %s ORDER BY nama_ujian", (selected_kompetensi,))
        nama_ujian_options = [row[0] for row in cur.fetchall()]
        st.markdown('<div class="custom-label">Filter Nama Ujian</div>', unsafe_allow_html=True)

        selected_nama_ujian = st.selectbox(
            label="",  # ⬅️ Kosongkan label asli
            options=["Semua"] + nama_ujian_options,
            key="filter_nama_ujian"
)

    with col2:
        st.markdown('<div class="custom-label">Urutkan Nilai</div>', unsafe_allow_html=True)
        sort_akhir = st.radio("", ["📈 Tertinggi", "📉 Terkecil"], horizontal=True, key="sort_nilai")

    # Query dan Tampilan Data
    query = """
    SELECT 
        n.username,
        nu.nama_ujian,
        n.nilai_akhir,
        n.waktu_nilai
    FROM nilai_akhir_mahasiswa n
    JOIN nama_ujian nu ON n.id_ujian = nu.id_ujian
    WHERE nu.kompetensi = %s
    """
    params = [selected_kompetensi]

    if selected_nama_ujian != "Semua":
        query += " AND nu.nama_ujian = %s"
        params.append(selected_nama_ujian)

    query += " ORDER BY n.nilai_akhir"
    query += " DESC" if sort_akhir == "📈 Tertinggi" else " ASC"

    cur.execute(query, tuple(params))
    hasil = cur.fetchall()

    if hasil:
        df_akhir = pd.DataFrame(hasil, columns=["Username", "Nama Ujian", "Nilai Akhir", "Waktu Dinilai"])
        
        # Display data
        st.dataframe(df_akhir, use_container_width=True, height=400)

        # Enhanced Statistics Section
        st.markdown("---")
        st.markdown('<div style="text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; color: #1f77b4;">📊 Ringkasan Statistik Nilai</div>', unsafe_allow_html=True)
        
        # Calculate statistics
        avg_score = df_akhir["Nilai Akhir"].mean()
        max_score = df_akhir["Nilai Akhir"].max()
        min_score = df_akhir["Nilai Akhir"].min()
        
        # Find students with highest and lowest scores
        top_student = df_akhir[df_akhir["Nilai Akhir"] == max_score]["Username"].iloc[0]
        bottom_student = df_akhir[df_akhir["Nilai Akhir"] == min_score]["Username"].iloc[0]
        
        # Enhanced Statistics Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 25px; border-radius: 20px; text-align: center; 
                        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3); 
                        margin-bottom: 20px; border: 2px solid rgba(255,255,255,0.1);">
                <div style="background: rgba(255,255,255,0.2); 
                           border-radius: 50%; width: 60px; height: 60px; 
                           margin: 0 auto 15px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 28px;">📊</span>
                </div>
                <h3 style="color: white; margin: 0; font-size: 16px; font-weight: 500;">Rata-rata Nilai</h3>
                <h1 style="color: white; margin: 15px 0 5px; font-size: 36px; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{avg_score:.1f}</h1>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 8px 16px; border-radius: 20px; margin-top: 10px;">
                    <p style="color: #e8f0ff; margin: 0; font-size: 13px; font-weight: 500;">Performa Keseluruhan</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 25px; border-radius: 20px; text-align: center; 
                        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3); 
                        margin-bottom: 20px; border: 2px solid rgba(255,255,255,0.1);">
                <div style="background: rgba(255,255,255,0.2); 
                           border-radius: 50%; width: 60px; height: 60px; 
                           margin: 0 auto 15px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 28px;">🏆</span>
                </div>
                <h3 style="color: white; margin: 0; font-size: 16px; font-weight: 500;">Nilai Tertinggi</h3>
                <h1 style="color: white; margin: 15px 0 5px; font-size: 36px; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{max_score}</h1>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 8px 16px; border-radius: 20px; margin-top: 10px;">
                    <p style="color: #ffe8f0; margin: 0; font-size: 13px; font-weight: 500;">👤 {top_student}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 25px; border-radius: 20px; text-align: center; 
                        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.3); 
                        margin-bottom: 20px; border: 2px solid rgba(255,255,255,0.1);">
                <div style="background: rgba(255,255,255,0.2); 
                           border-radius: 50%; width: 60px; height: 60px; 
                           margin: 0 auto 15px; display: flex; align-items: center; justify-content: center;">
                    <span style="font-size: 28px;">📉</span>
                </div>
                <h3 style="color: white; margin: 0; font-size: 16px; font-weight: 500;">Nilai Terendah</h3>
                <h1 style="color: white; margin: 15px 0 5px; font-size: 36px; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">{min_score}</h1>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 8px 16px; border-radius: 20px; margin-top: 10px;">
                    <p style="color: #e8f8ff; margin: 0; font-size: 13px; font-weight: 500;">👤 {bottom_student}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        
        # Score Distribution Analysis
        st.markdown("---")
        st.markdown('<div style="text-align: center; font-size: 20px; font-weight: bold; margin: 20px 0; color: #1f77b4;">🎯 Analisis Distribusi Nilai</div>', unsafe_allow_html=True)
        
        # Categorize scores
        excellent = len(df_akhir[df_akhir["Nilai Akhir"] >= 85])
        good = len(df_akhir[(df_akhir["Nilai Akhir"] >= 70) & (df_akhir["Nilai Akhir"] < 85)])
        average = len(df_akhir[(df_akhir["Nilai Akhir"] >= 60) & (df_akhir["Nilai Akhir"] < 70)])
        poor = len(df_akhir[df_akhir["Nilai Akhir"] < 60])
        total_students = len(df_akhir)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            percentage = (excellent/total_students*100) if total_students > 0 else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #00b894, #00cec9); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3); 
                        margin-bottom: 15px; transform: scale(1.02);">
                <div style="font-size: 24px; margin-bottom: 10px;">🌟</div>
                <h4 style="color: white; margin: 0; font-size: 14px; font-weight: 600;">Sangat Baik</h4>
                <h4 style="color: #e0f7fa; margin: 0; font-size: 12px;">(≥85)</h4>
                <h2 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{excellent}</h2>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 5px 10px; border-radius: 10px;">
                    <p style="color: #e0f7fa; margin: 0; font-size: 12px; font-weight: 500;">{percentage:.1f}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            percentage = (good/total_students*100) if total_students > 0 else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fdcb6e, #e17055); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(253, 203, 110, 0.3); 
                        margin-bottom: 15px;">
                <div style="font-size: 24px; margin-bottom: 10px;">✨</div>
                <h4 style="color: white; margin: 0; font-size: 14px; font-weight: 600;">Baik</h4>
                <h4 style="color: #fff3e0; margin: 0; font-size: 12px;">(70-84)</h4>
                <h2 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{good}</h2>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 5px 10px; border-radius: 10px;">
                    <p style="color: #fff3e0; margin: 0; font-size: 12px; font-weight: 500;">{percentage:.1f}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            percentage = (average/total_students*100) if total_students > 0 else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #74b9ff, #0984e3); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.3); 
                        margin-bottom: 15px;">
                <div style="font-size: 24px; margin-bottom: 10px;">📊</div>
                <h4 style="color: white; margin: 0; font-size: 14px; font-weight: 600;">Cukup</h4>
                <h4 style="color: #e3f2fd; margin: 0; font-size: 12px;">(60-69)</h4>
                <h2 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{average}</h2>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 5px 10px; border-radius: 10px;">
                    <p style="color: #e3f2fd; margin: 0; font-size: 12px; font-weight: 500;">{percentage:.1f}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            percentage = (poor/total_students*100) if total_students > 0 else 0
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #fd79a8, #e84393); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(253, 121, 168, 0.3); 
                        margin-bottom: 15px;">
                <div style="font-size: 24px; margin-bottom: 10px;">⚠️</div>
                <h4 style="color: white; margin: 0; font-size: 14px; font-weight: 600;">Perlu Perbaikan</h4>
                <h4 style="color: #fce4ec; margin: 0; font-size: 12px;">(<60)</h4>
                <h2 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{poor}</h2>
                <div style="background: rgba(255,255,255,0.2); 
                           padding: 5px 10px; border-radius: 10px;">
                    <p style="color: #fce4ec; margin: 0; font-size: 12px; font-weight: 500;">{percentage:.1f}%</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Download button
        st.markdown("---")
        csv_akhir = df_akhir.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Nilai Akhir",
            data=csv_akhir,
            file_name=f"nilai_akhir_{selected_kompetensi.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("ℹ️ Belum ada data nilai akhir untuk kompetensi ini.")

elif menu_option == "📈 Rekap Detail":
    st.markdown('<div class="section-header">📈 Rekap Detail Nilai Mahasiswa</div>', unsafe_allow_html=True)
    
    # Filter Controls
    cur.execute("""
        SELECT nu.id_ujian, nu.nama_ujian, 
               COALESCE(nu.tanggal_mulai, CURRENT_TIMESTAMP) as tanggal
        FROM nama_ujian nu
        WHERE nu.kompetensi = %s
        ORDER BY tanggal DESC
    """, (selected_kompetensi,))
    ujian_list = cur.fetchall()
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="color:#264653; font-weight:600; font-size:15px; margin-bottom:-150px;">
            📄 Filter berdasarkan Nama Ujian
        </div>
    """, unsafe_allow_html=True)

        selected_ujian_filter = st.selectbox(
            "",
            options=[None] + ujian_list,
            format_func=lambda x: f"{x[1]} - {x[2].strftime('%d %B %Y') if x[2] else 'Tanggal tidak tersedia'}" if x else "Semua Ujian",
            key="filter_ujian_rekap"
        )
    with col2:
        st.markdown("""
        <div style="color:#264653; font-weight:600; font-size:15px; margin-bottom:-150px;">
            📊 Urutkan Berdasarkan Nilai
        </div>
    """, unsafe_allow_html=True)
        sort_order = st.radio(
            "",
            options=["📈 Tertinggi", "📉 Terkecil"],
            horizontal=True,
            key="sort_rekap"
        )
    
    # Query dan Tampilan Data
    query = """
        SELECT 
            jm.username,
            nu.nama_ujian,
            s.pertanyaan,
            jm.jawaban,
            jm.skor_keyword,
            jm.skor_llm,
            jm.skor_final,
            jm.waktu_submit
        FROM jawaban_mahasiswa jm
        JOIN list_soal s ON jm.id_question = s.id_question
        JOIN nama_ujian nu ON jm.id_ujian = nu.id_ujian
        WHERE s.kompetensi = %s
    """
    params = [selected_kompetensi]
    
    if selected_ujian_filter:
        query += " AND nu.id_ujian = %s"
        params.append(selected_ujian_filter[0])
    
    query += " ORDER BY jm.skor_final"
    query += " DESC" if sort_order == "📈 Tertinggi" else " ASC"
    
    cur.execute(query, tuple(params))
    hasil = cur.fetchall()
    
    if hasil:
        df = pd.DataFrame(
            hasil,
            columns=["Mahasiswa", "Nama Ujian", "Pertanyaan", "Jawaban", "Skor Keyword", "Skor LLM", "Skor Akhir", "Waktu Submit" ]
        )
        
        # Display data
        st.dataframe(df, use_container_width=True, height=500)
        
        # Enhanced Statistics Section
        st.markdown("---")
        st.markdown('<div style="text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0; color: #1f77b4;">📊 Ringkasan Statistik</div>', unsafe_allow_html=True)
        
        # Calculate statistics
        rata_rata = df["Skor Akhir"].mean()
        skor_tertinggi = df["Skor Akhir"].max()
        skor_terendah = df["Skor Akhir"].min()
        median_skor = df["Skor Akhir"].median()
        std_dev = df["Skor Akhir"].std()
        total_mahasiswa = df["Mahasiswa"].nunique()
        total_soal = len(df)
        
        # Main Statistics Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h3 style="color: white; margin: 0; font-size: 16px;">📊 Rata-rata Skor</h3>
                <h1 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{rata_rata:.1f}</h1>
                <p style="color: #e0e0e0; margin: 0; font-size: 12px;">dari total {total_soal} jawaban</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h3 style="color: white; margin: 0; font-size: 16px;">🏆 Skor Tertinggi</h3>
                <h1 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{skor_tertinggi}</h1>
                <p style="color: #e0e0e0; margin: 0; font-size: 12px;">nilai maksimal</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        padding: 20px; border-radius: 15px; text-align: center; 
                        box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;">
                <h3 style="color: white; margin: 0; font-size: 16px;">📉 Skor Terendah</h3>
                <h1 style="color: white; margin: 10px 0; font-size: 32px; font-weight: bold;">{skor_terendah}</h1>
                <p style="color: #e0e0e0; margin: 0; font-size: 12px;">nilai minimal</p>
            </div>
            """, unsafe_allow_html=True)
        
        
        # Download CSV
        st.markdown("---")
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Rekap Detail",
            data=csv_data,
            file_name=f"rekap_detail_{selected_kompetensi.lower().replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    else:
        st.info("ℹ️ Belum ada data jawaban untuk kompetensi ini.")


# FOOTER
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #718096; font-size: 0.9rem; margin-top: 2rem; opacity: 0.8;">
    <p>🎓 Dashboard Dosen - Sistem Manajemen Ujian</p>
    <p>Kompetensi Aktif: <strong>{selected_kompetensi}</strong></p>
</div>
""", unsafe_allow_html=True)

cur.close()
conn.close()