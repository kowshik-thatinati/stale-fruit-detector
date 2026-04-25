import streamlit as st
import base64
from translation import TRANSLATIONS
from utils.style import apply_style

# Set page config - MUST be first Streamlit command
st.set_page_config(page_title="Stale Fruit Detector", layout="wide")

# Apply custom background color with !important flag and additional selectors
st.markdown("""
    <style>
    .stApp {
        background-color: #FEF9EF !important;
    }
    
    /* Ensure the color is applied to all main containers */
    .main {
        background-color: #FEF9EF !important;
    }
    
    .stMarkdown {
        background-color: transparent;
    }
    
    /* Make glass cards more visible against the background */
    .glass-card {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)

# Apply shared styles
apply_style()

# --- Language Selection ---
lang = st.sidebar.selectbox("🌐 Select Language", ["English", "Telugu", "Hindi"])
tr = TRANSLATIONS["main"][lang]

# Main Content
st.markdown(
    f'''
    <div style="
        text-align: center;
        margin: 2rem auto;
        max-width: 800px;
        background: linear-gradient(135deg, #FFF6E5, #FFF9EC);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);">
        <h1 style="
            color: #2C3E50;
            font-size: 2.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            {tr["title"]}
        </h1>
        <p style="
            color: #666;
            font-size: 1.1rem;
            line-height: 1.6;
            max-width: 600px;
            margin: 0 auto;">
            {tr["desc1"]}
        </p>
    </div>
    ''',
    unsafe_allow_html=True
)

# Feature Cards
st.markdown(
    f'''
    <div class="card-grid">
        <div class="glass-card">
            <h3>🤖 AI-Powered Detection</h3>
            <p>{tr["desc2"]}</p>
        </div>
        <div class="glass-card">
            <h3>⚡ Instant Results</h3>
            <p>{tr["scan_line"]}</p>
        </div>
        <div class="glass-card">
            <h3>📊 Detailed Analysis</h3>
            <p>{tr["desc1"]}</p>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# How It Works Section
st.markdown(
    '''
    <div class="glass-card">
        <h2>How It Works</h2>
        <div style="margin: 20px 0;">
            <h4>1. Upload Your Image 📸</h4>
            <p>Take a clear photo of your fruit or upload an existing image</p>
        </div>
        <div style="margin: 20px 0;">
            <h4>2. AI Analysis 🔍</h4>
            <p>Our advanced AI models analyze the image for signs of freshness</p>
        </div>
        <div style="margin: 20px 0;">
            <h4>3. Get Results 📋</h4>
            <p>Receive instant feedback and storage recommendations</p>
        </div>
    </div>
    ''',
    unsafe_allow_html=True
)

# Call to Action
st.markdown(
    '''
    <div class="glass-card" style="text-align: center;">
        <h2>Get Started Today</h2>
        <p style="margin: 20px 0;">Sign up or log in to start detecting fruit freshness</p>
    </div>
    ''',
    unsafe_allow_html=True
)