import streamlit as st
from config.db_config import get_connection
from datetime import datetime
import requests
import time

# =============== HIDE DEFAULT SIDEBAR NAVIGATION ===============
hide_nav_style = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_nav_style, unsafe_allow_html=True)

# ================================
# Page Configuration
# ================================
st.set_page_config(
    page_title="Dashboard Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS dengan kontras warna yang diperbaiki
st.markdown("""
<style>
    /* Force light theme background */
    .stApp {
        background-color: #f8f9fa !important;
    }
    
    .main > div {
        background-color: #f8f9fa !important;
    }
    
    /* SIDEBAR STYLING - PERBAIKAN KONTRAS */
    .css-1d391kg, .css-1lcbmhc, .css-17eq0hr, [data-testid="stSidebar"] {
        background-color: #2c3e50 !important; /* Background gelap */
    }
    
    /* Sidebar text styling - TEKS TERANG UNTUK KONTRAS */
    .css-1d391kg .stMarkdown, 
    .css-1d391kg .stMarkdown p,
    .css-1d391kg .stMarkdown h3,
    .css-1d391kg .stMarkdown h4,
    .css-1d391kg .stMarkdown strong,
    .css-1d391kg .stMarkdown small,
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown h3,
    [data-testid="stSidebar"] .stMarkdown strong,
    [data-testid="stSidebar"] .stMarkdown small {
        color: #ffffff !important; /* Teks putih untuk kontras */
    }
    
    /* Sidebar metric styling */
    [data-testid="stSidebar"] .stMetric,
    [data-testid="stSidebar"] .stMetric label,
    [data-testid="stSidebar"] .stMetric div {
        color: #ffffff !important;
    }
    
    /* Sidebar button styling */
    [data-testid="stSidebar"] .stButton button {
        background-color: #e74c3c !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: background-color 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #c0392b !important;
    }
    
    /* MAIN CONTENT STYLING */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .welcome-card {
        background: #ffffff; /* Background putih */
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px solid #e9ecef;
        margin-bottom: 1rem;
        color: #212529; /* Teks gelap untuk kontras */
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .exam-card {
        background: #ffffff; /* Background putih */
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        color: #212529; /* Teks gelap untuk kontras */
        border: 1px solid #dee2e6;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 1.5rem 0;
        gap: 1rem;
        flex-wrap: wrap;
    }
    
    .stat-item {
        text-align: center;
        padding: 1.5rem;
        background: #ffffff; /* Background putih */
        border-radius: 12px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.1);
        min-width: 120px;
        border: 2px solid #e9ecef;
        color: #212529; /* Teks gelap untuk kontras */
        transition: transform 0.2s ease;
    }
    
    .stat-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
    }
    
    .emoji-large {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* QUESTION STYLING - TANPA BOX */
    .question-text {
        color: #1d3557 !important;
        font-size: 1.3rem !important;
        font-weight: 600 !important;
        margin: 2rem 0 1rem 0 !important;
        line-height: 1.4 !important;
    }
    
    /* LIST STYLING */
    .exam-list {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 0;
        margin: 1rem 0;
    }
    
    .exam-list-item {
        padding: 1rem 1.5rem;
        border-bottom: 1px solid #e9ecef;
        color: #212529;
        transition: background-color 0.2s ease;
    }
    
    .exam-list-item:last-child {
        border-bottom: none;
    }
    
    .exam-list-item:hover {
        background-color: #f8f9fa;
    }
    
    /* FORM STYLING - PERBAIKAN KONTRAS */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 0.2rem rgba(102,126,234,0.25) !important;
    }
    
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #212529 !important;
        border: 2px solid #ced4da !important;
    }
    
    /* BUTTON STYLING */
    .stButton button[kind="primary"] {
        background: linear-gradient(45deg, #667eea, #764ba2) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(102,126,234,0.4) !important;
    }
    
    .stButton button[kind="secondary"] {
        background-color: #6c757d !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* MAIN CONTENT TEXT STYLING - FIXED */
    .stApp .main .stMarkdown,
    .stApp .main .stMarkdown p,
    .stApp .main .stMarkdown h1,
    .stApp .main .stMarkdown h2,
    .stApp .main .stMarkdown h3,
    .stApp .main .stMarkdown h4,
    .stApp .main .stMarkdown strong,
    .stApp .main .stMarkdown small {
        color: #212529 !important;
    }
    
    /* SUBMIT BUTTON STYLING */
    .submit-section {
        background: linear-gradient(135deg, #28a745, #20c997);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(40,167,69,0.3);
    }
    
    .submit-section h3 {
        color: white !important;
        margin-bottom: 1rem;
    }
    
    .submit-section p {
        color: white !important;
        margin-bottom: 1.5rem;
    }
    
    /* SCORE RESULT STYLING - DIPERBAIKI */
    .score-result {
        background: linear-gradient(135deg, #667eea, #764ba2);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
        color: white !important;
        box-shadow: 0 4px 15px rgba(102,126,234,0.3);
    }
    
    .score-result h1, .score-result h2, .score-result h3, .score-result p, .score-result small {
        color: white !important;
    }
    
    /* EXPANDER STYLING - TAMBAHAN BARU */
    .stExpander {
        background-color: #ffffff !important;
        border: 1px solid #dee2e6 !important;
        border-radius: 8px !important;
        margin: 1rem 0 !important;
    }
    
    .stExpander .streamlit-expanderHeader {
        background-color: #f8f9fa !important;
        color: #212529 !important;
        font-weight: 600 !important;
        border-radius: 8px 8px 0 0 !important;
    }
    
    .stExpander .streamlit-expanderContent {
        background-color: #ffffff !important;
        color: #212529 !important;
        padding: 1rem !important;
    }
    
    /* DETAIL JAWABAN STYLING - TAMBAHAN BARU */
    .stExpander .stMarkdown p,
    .stExpander .stMarkdown strong,
    .stExpander .stMarkdown small {
        color: #212529 !important;
    }
    
    /* Khusus untuk expander content - TAMBAHAN BARU */
    .stApp .main .stExpander .stMarkdown,
    .stApp .main .stExpander .stMarkdown p,
    .stApp .main .stExpander .stMarkdown strong,
    .stApp .main .stExpander .stMarkdown small {
        color: #212529 !important;
    }
    
    /* Override untuk semua elemen di dalam expander - TAMBAHAN BARU */
    [data-testid="stExpander"] * {
        color: #212529 !important;
    }
    
    [data-testid="stExpander"] .element-container * {
        color: #212529 !important;
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
            
    /* Kurangi jarak antara label dct */
    .custom-label {
        margin-bottom: -150px;
        font-weight: 600;
        font-size: 16px;
        color: #264653;
    }
</style>
""", unsafe_allow_html=True)

# ================================
# Header Section
# ================================
st.markdown("""
<div class="main-header">
    <h1>🎓 Dashboard Mahasiswa</h1>
    <p>Platform Ujian Online Terpadu</p>
</div>
""", unsafe_allow_html=True)

# ================================
# Authentication Check
# ================================
if st.session_state.get("role") != "mahasiswa":
    st.error("🚫 Akses hanya untuk mahasiswa.")
    st.info("Silakan login dengan akun mahasiswa untuk melanjutkan.")
    st.stop()

username = st.session_state.get('username', 'Guest')

# Welcome Card
st.markdown(f"""
<div class="welcome-card">
    <h3>👋 Selamat Datang, {username}!</h3>
    <p>Siap untuk mengerjakan ujian hari ini? Mari kita mulai!</p>
</div>
""", unsafe_allow_html=True)

# ================================
# Database Connection
# ================================
try:
    conn = get_connection()
    cur = conn.cursor()
except Exception as e:
    st.error(f"❌ Gagal terhubung ke database: {e}")
    st.stop()

# ================================
# Sidebar - Navigation & Info
# ================================
with st.sidebar:
    st.markdown("### 📋 Menu Navigasi")
    st.markdown("---")
    
    # User info
    st.markdown(f"**👤 Pengguna:** {username}")
    st.markdown(f"**📅 Tanggal:** {datetime.now().strftime('%d %B %Y')}")
    st.markdown(f"**⏰ Waktu:** {datetime.now().strftime('%H:%M WIB')}")
    st.markdown("---")
    
    # Quick stats
    st.markdown("### 📊 Statistik Cepat")
    
    # Hitung total ujian yang pernah diikuti
    cur.execute("""
        SELECT COUNT(DISTINCT id_ujian) 
        FROM jawaban_mahasiswa 
        WHERE username = %s
    """, (username,))
    total_ujian_selesai = cur.fetchone()[0] or 0
    
    st.metric("Ujian Selesai", total_ujian_selesai)
    
    # Logout button
    st.markdown("---")
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.success("✅ Berhasil logout. Mengalihkan ke halaman login...")
        st.switch_page("pages/login.py")

# ================================
# 1. Pilih Ujian Aktif (LIST FORMAT)
# ================================
col1, col2 = st.columns([2, 1])

st.markdown("""<h2 style='color:#1d3557; margin-top: -4.5rem;'>📘 Ujian yang Tersedia</h2>""", unsafe_allow_html=True)

with col2:
    if st.button("🔄 Refresh", help="Refresh daftar ujian"):
        st.rerun()

cur.execute("""
    SELECT id_ujian, nama_ujian, tanggal_mulai, tanggal_selesai
    FROM nama_ujian
    WHERE aktif = TRUE AND tanggal_mulai <= CURRENT_DATE 
    ORDER BY tanggal_mulai DESC
""")
ujian_aktif = cur.fetchall()

if not ujian_aktif:
    st.markdown("""
    <div class="exam-card">
        <div style="text-align: center; padding: 2rem;">
            <div class="emoji-large">📚</div>
            <h3>Tidak Ada Ujian Aktif</h3>
            <p>Belum ada ujian yang tersedia saat ini. Silakan periksa kembali nanti.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Display available exams as list
selected_ujian = st.selectbox(
    "Pilih Ujian:",
    ujian_aktif,
    format_func=lambda x: f"📝 {x[1]} - {x[2]}",
    help="Pilih ujian yang ingin dikerjakan"
)

id_ujian = selected_ujian[0]
nama_ujian = selected_ujian[1]

# Display selected exam info
st.markdown(f"""
<div class="exam-card">
    <h4>📋 {nama_ujian}</h4>
    <p><strong>📅 Periode:</strong> {selected_ujian[2]} s/d {selected_ujian[3]}</p>
</div>
""", unsafe_allow_html=True)

# ================================
# 2. Ambil Soal dari Ujian
# ================================
cur.execute("""
    SELECT s.id_question, s.pertanyaan
    FROM soal_ujian su
    JOIN list_soal s ON su.id_question = s.id_question
    WHERE su.id_ujian = %s
    ORDER BY s.id_question
""", (id_ujian,))
soal_ujian = cur.fetchall()

if not soal_ujian:
    st.warning("⚠️ Belum ada soal dalam ujian ini.")
    st.stop()

total_soal = len(soal_ujian)

# Check if already submitted
cur.execute("""
    SELECT COUNT(*) FROM jawaban_mahasiswa
    WHERE username = %s AND id_ujian = %s
""", (username, id_ujian))
sudah_submit = cur.fetchone()[0] > 0

if sudah_submit:
    # Show results if already submitted
    cur.execute("""
        SELECT skor_final FROM jawaban_mahasiswa
        WHERE username = %s AND id_ujian = %s
    """, (username, id_ujian))
    semua_skor = cur.fetchall()
    
    total_nilai = sum(s[0] for s in semua_skor)
    final_nilai = round((total_nilai / (total_soal * 5)) * 100)
    
    # Determine grade and message
    if final_nilai >= 85:
        grade = "A"
        message = "Luar biasa! 🌟"
        color = "#28a745"
    elif final_nilai >= 70:
        grade = "B"
        message = "Bagus sekali! 👏"
        color = "#17a2b8"
    elif final_nilai >= 60:
        grade = "C"
        message = "Cukup baik! 👍"
        color = "#ffc107"
    else:
        grade = "D"
        message = "Perlu belajar lebih giat! 💪"
        color = "#dc3545"
    
    st.markdown(f"""
    <div class="score-result">
        <h2>🎓 Ujian Telah Selesai!</h2>
        <h1 style="font-size: 3rem; margin: 1rem 0;">{final_nilai}/100</h1>
        <h3>Grade: {grade}</h3>
        <p style="font-size: 1.2rem; margin-top: 1rem;">{message}</p>
        <small>Total Poin: {total_nilai}/{total_soal * 5}</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Show detailed answers
    with st.expander("📊 Lihat Detail Jawaban"):
        cur.execute("""
            SELECT jm.jawaban, jm.skor_final, ls.pertanyaan
            FROM jawaban_mahasiswa jm
            JOIN list_soal ls ON jm.id_question = ls.id_question
            WHERE jm.username = %s AND jm.id_ujian = %s
            ORDER BY jm.id_question
        """, (username, id_ujian))
        detail_jawaban = cur.fetchall()
        
        for i, (jawaban, skor, pertanyaan) in enumerate(detail_jawaban, 1):
            st.markdown(f"**Soal {i}:** {pertanyaan}")
            st.markdown(f"**Jawaban:** {jawaban}")
            st.markdown(f"**Skor:** {skor}/5")
            st.markdown("---")
    
    st.stop()

# Statistics for current exam
st.markdown(f"""
<div class="stats-container">
    <div class="stat-item">
        <div class="emoji-large">📝</div>
        <strong>{total_soal}</strong><br>
        <small>Total Soal</small>
    </div>
    <div class="stat-item">
        <div class="emoji-large">⏱️</div>
        <strong>Unlimited</strong><br>
        <small>Waktu</small>
    </div>
    <div class="stat-item">
        <div class="emoji-large">🎯</div>
        <strong>Essay</strong><br>
        <small>Tipe Soal</small>
    </div>
</div>
""", unsafe_allow_html=True)

# ================================
# 3. Form Jawaban Semua Soal Sekaligus
# ================================
st.markdown('<div class="section-title">📝 Jawab Semua Pertanyaan</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-label">Catatan: Pastikan semua soal telah dijawab sebelum submit!</div>', unsafe_allow_html=True)

# Single form for all questions
with st.form("form_ujian_lengkap", clear_on_submit=False):
    jawaban_dict = {}
    
    for idx, (id_question, pertanyaan) in enumerate(soal_ujian, 1):
        # Display question without box - larger text
        st.markdown(f"""
        <p class="question-text">Soal {idx}. {pertanyaan}</p>
        """, unsafe_allow_html=True)
        
        # Answer input
        jawaban = st.text_area(
            f"Jawaban untuk Soal {idx}:",
            height=120,
            placeholder="Ketikkan jawaban Anda di sini...",
            help="Berikan jawaban yang lengkap dan jelas",
            key=f"jawab_{id_question}"
        )
        
        jawaban_dict[id_question] = {
            'jawaban': jawaban,
            'pertanyaan': pertanyaan
        }
        
        st.markdown("<br>", unsafe_allow_html=True)
    
    # Submit section
    st.markdown("""
    <div class="submit-section">
        <h3>🚀 Siap Submit Ujian?</h3>
        <p>Pastikan semua jawaban sudah lengkap dan benar!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_all = st.form_submit_button(
            "📤 SUBMIT SEMUA JAWABAN",
            use_container_width=True,
            type="primary"
        )

    if submit_all:
        # Validate all answers
        empty_answers = []
        for idx, (id_question, data) in enumerate(jawaban_dict.items(), 1):
            if not data['jawaban'].strip():
                empty_answers.append(f"Soal {idx}")
        
        if empty_answers:
            st.error(f"❌ Jawaban berikut masih kosong: {', '.join(empty_answers)}")
        else:
            # Process all answers
            with st.spinner("🤔 Sedang menilai semua jawaban Anda..."):
                try:
                    progress_bar = st.progress(0)
                    total_progress = len(jawaban_dict)
                    processed = 0
                    
                    # Process each answer
                    for id_question, data in jawaban_dict.items():
                        response = requests.post("http://127.0.0.1:8000/score", json={
                            "pertanyaan": data['pertanyaan'],
                            "jawaban": data['jawaban'],
                            "id_soal": id_question
                        }, timeout=30)
                        
                        if response.status_code == 200:
                            result = response.json()
                            skor_llm = result["llm_score"]
                            skor_keyword = result["keyword_score"]
                            skor_final = result["final_score"]

                            cur.execute("""
                                INSERT INTO jawaban_mahasiswa (
                                    username, id_ujian, id_question, jawaban,
                                    skor_keyword, skor_llm, skor_final, waktu_submit
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                username, id_ujian, id_question, data['jawaban'],
                                skor_keyword, skor_llm, skor_final, datetime.now()
                            ))
                        else:
                            st.error(f"❌ Gagal menilai soal {id_question}")
                            st.stop()
                        
                        processed += 1
                        progress_bar.progress(processed / total_progress)
                    
                    conn.commit()
                    st.success("🎉 Semua jawaban berhasil disimpan!")
                    time.sleep(2)
                    st.rerun()
                    
                except requests.exceptions.Timeout:
                    st.error("⏰ Timeout: Server terlalu lama merespons. Silakan coba lagi.")
                except requests.exceptions.ConnectionError:
                    st.error("🔌 Gagal terhubung ke server penilaian. Periksa koneksi internet Anda.")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

# ================================
# Cleanup
# ================================
try:
    cur.close()
    conn.close()
except:
    pass

# ================================
# Footer
# ================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>📚 Sistem Ujian Online | Dibuat dengan ❤️ untuk pendidikan yang lebih baik</small>
</div>
""", unsafe_allow_html=True)