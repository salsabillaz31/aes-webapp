import streamlit as st
from config.db_config import get_connection
from utils.auth import check_login

# ====================== CONFIG & HIDE ELEMENTS ======================
st.set_page_config(page_title="Login - AES", page_icon="📝", layout="wide")

st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    header, footer {
        visibility: hidden;
    }
    
    /* Main container styling */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Center the main content */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    
    /* Title styling */
    .main-title {
        font-size: 3rem !important;
        color: #2C499B !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        font-weight: bold !important;
    }
    
    .sub-title {
        font-size: 1.5rem !important;
        color: #666 !important;
        text-align: center !important;
        margin-bottom: 3rem !important;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        height: 3.5rem !important;
        font-size: 1.1rem !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        font-weight: 400 !important;
        padding: 0 1.5rem !important;
        border: 2px solid #ddd !important;
        border-radius: 12px !important;
        background-color: white !important;
        color: #333 !important;
        line-height: 1.5 !important;
        vertical-align: middle !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* Override Streamlit's default dark input styling */
    .stTextInput > div > div > input[data-baseweb="input"] {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #ddd !important;
    }
    
    /* Target specific input states */
    .stTextInput input {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #ddd !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3BBEEE !important;
        box-shadow: 0 0 10px rgba(59, 190, 238, 0.3) !important;
        outline: none !important;
        background-color: white !important;
        color: #333 !important;
    }
    
    .stTextInput > label {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        color: #333 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Fix input placeholder and text styling */
    .stTextInput > div > div > input::placeholder {
        color: #999 !important;
        opacity: 1 !important;
        font-size: 1.1rem !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Remove any unwanted input decorations */
    .stTextInput > div > div > input::-webkit-input-placeholder {
        color: #999 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .stTextInput > div > div > input::-moz-placeholder {
        color: #999 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    .stTextInput > div > div > input:-ms-input-placeholder {
        color: #999 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
    }
    
    /* Fix text alignment and positioning */
    .stTextInput > div > div {
        display: flex !important;
        align-items: center !important;
    }
    
    /* Force override any dark theme styling */
    div[data-testid="stTextInput"] > div > div > input {
        background-color: white !important;
        color: #333 !important;
        border: 2px solid #ddd !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #3BBEEE, #2196F3) !important;
        color: white !important;
        font-weight: bold !important;
        font-size: 1.3rem !important;
        padding: 1rem 2rem !important;
        border-radius: 12px !important;
        border: none !important;
        width: 100% !important;
        height: 3.5rem !important;
        margin-top: 2rem !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2196F3, #1976D2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 190, 238, 0.4) !important;
    }
    
    /* Image container */
    .image-container {
        text-align: center;
        padding: 2rem;
    }
    
    .login-image {
        width: 100% !important;
        max-width: 400px !important;
        height: auto !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
        margin-bottom: 2rem !important;
    }
    
    .welcome-text {
        font-size: 2rem !important;
        color: #2C499B !important;
        text-align: center !important;
        margin-top: 1rem !important;
        font-weight: 600 !important;
    }
    
    .description-text {
        font-size: 1.1rem !important;
        color: #666 !important;
        text-align: center !important;
        margin-top: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Form container styling */
    .login-form-container {
        background: white !important;
        padding: 2.5rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1) !important;
        margin: 2rem 0 !important;
    }
    
    /* Target the specific form elements inside container */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] .stTextInput,
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] .stButton {
        margin-bottom: 1rem !important;
    }
    
    /* Alert styling */
    .stAlert {
        font-size: 1.1rem !important;
        padding: 1rem !important;
        border-radius: 8px !important;
        margin-top: 1rem !important;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem !important;
        }
        .login-form-container {
            padding: 2rem !important;
            margin: 1rem 0 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ====================== CEK LOGIN ======================
if "username" in st.session_state and "role" in st.session_state:
    if st.session_state["role"] == "dosen":
        st.switch_page("pages/dashboard_dosen.py")
    elif st.session_state["role"] == "mahasiswa":
        st.switch_page("pages/dashboard_mahasiswa.py")

# ====================== HEADER ======================
st.markdown("<h1 class='main-title'>🎓 Sistem Penilaian Esai Otomatis</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Automated Essay Scoring System</p>", unsafe_allow_html=True)

# ====================== LOGIN FORM ======================
col1, col2 = st.columns([7, 5], gap="large")

with col1:
    # Image section - Using st.image instead of HTML
    try:
        st.image("assets/image/login.jpg", width=400, use_container_width=True)
    except:
        # Fallback if image not found
        st.markdown("""
            <div style="text-align: center; padding: 2rem;">
                <div style="width: 400px; height: 300px; background: linear-gradient(135deg, #3BBEEE, #2196F3); 
                            border-radius: 15px; display: flex; align-items: center; justify-content: center; 
                            margin: 0 auto; color: white; font-size: 1.5rem; font-weight: bold;">
                    🎓 Login Image
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 class="welcome-text">Selamat Datang!</h2>
            <p class="description-text">
                Masuk ke sistem untuk mengakses fitur penilaian esai otomatis 
                dengan teknologi AI yang canggih dan akurat.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    # Spacing untuk menengahkan form
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Login form title
    st.markdown("<h3 style='text-align: center; color: #2C499B; margin-bottom: 2rem;'>Masuk ke Sistem</h3>", unsafe_allow_html=True)
    
    # Login form tanpa box/container
    username = st.text_input(
        "👤 Username", 
        placeholder="Masukkan username Anda",
        key="username_field"
    )
    
    password = st.text_input(
        "🔒 Password", 
        type="password", 
        placeholder="Masukkan password Anda",
        key="password_field"
    )

    if st.button("🚀 MASUK KE SISTEM", key="login_btn"):
        if username and password:
            try:
                conn = get_connection()
                role = check_login(username, password, conn)
                conn.close()

                if role:
                    st.session_state["username"] = username
                    st.session_state["role"] = role
                    st.success("✅ Login berhasil! Mengarahkan ke dashboard...")
                    if role == "dosen":
                        st.switch_page("pages/dashboard_dosen.py")
                    elif role == "mahasiswa":
                        st.switch_page("pages/dashboard_mahasiswa.py")
                else:
                    st.error("❌ Login gagal! Username atau password salah.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {str(e)}")
        else:
            st.warning("⚠️ Harap isi semua field yang diperlukan.")

# ====================== FOOTER INFO ======================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem; padding: 1rem;">
        <p>💡 <strong>Tips:</strong> Pastikan koneksi internet stabil untuk pengalaman terbaik</p>
        <p>📧 Butuh bantuan? Hubungi administrator sistem</p>
    </div>
""", unsafe_allow_html=True)