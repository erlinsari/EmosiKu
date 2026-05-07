import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman (Hapus Margin Streamlit)
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="collapsed")

# --- SUNTIKAN CSS KAMUFLASE (Menyamakan Elemen Asli dengan Desain Premium) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .block-container { padding: 0 !important; max-width: 100% !important; }
    
    /* KAMUFLASE KOTAK KETIK */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.1rem !important;
        color: #1e293b !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.02) !important;
    }
    
    /* KAMUFLASE TOMBOL ANALISIS (IDENTIK DENGAN DESAIN REACT) */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed 0%, #0891b2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        font-size: 1.1rem !important;
        box-shadow: 0 10px 40px rgba(139,92,246,0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        max-width: 350px;
        margin-top: -50px; /* Posisi Tombol agar pas */
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 50px rgba(139,92,246,0.5) !important;
    }

    /* Hilangkan Label Streamlit agar Bersih */
    [data-testid="stWidgetLabel"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

@st.cache_resource
def load_ai_engine():
    MODEL_NAME = "indobenchmark/indobert-lite-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

def analyze_emotion(text):
    tokenizer, model, stopword_remover = load_ai_engine()
    text = re.sub(r'http\S+|[^a-zA-Z\s]', '', str(text)).lower()
    cleaned = stopword_remover.remove(text).strip()
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True, max_length=64)
    with torch.no_grad():
        out = model(**inputs)
    probs = torch.softmax(out.logits, dim=-1)[0]
    pred = torch.argmax(out.logits, dim=-1).item()
    is_stable = pred == 0
    return {
        "status": 'Kondisi Stabil' if is_stable else 'Terindikasi Gangguan Psikologis',
        "sentiment": 'positive' if is_stable else 'negative',
        "description": 'Pola emosi Anda memancarkan keseimbangan. Pertahankan kesehatan mental Anda.' if is_stable 
                      else 'AI mendeteksi pola yang mengindikasikan kecemasan. Sangat disarankan untuk berbagi perasaan ini.',
        "wellness": int(probs[0] * 100),
        "stress": int(probs[1] * 100),
        "clarity": int(torch.max(probs) * 100),
        "energy": 85 if is_stable else 45,
        "originalText": text
    }

def get_premium_ui(result=None):
    try:
        index_path = os.path.join(DIST_DIR, "index.html")
        assets_dir = os.path.join(DIST_DIR, "assets")
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        js_files = glob.glob(os.path.join(assets_dir, "*.js"))
        css_files = glob.glob(os.path.join(assets_dir, "*.css"))
        result_json = json.dumps(result) if result else "null"
        injection = f'<script>window.initialResult = {result_json};</script>'
        with open(js_files[0], "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(css_files[0], "r", encoding="utf-8") as f:
            css_code = f.read()
        final_html = html_content.replace('<head>', f'<head>{injection}')
        final_html = final_html.replace('</head>', f'<style>{css_code}</style></head>')
        final_html = final_html.replace('</body>', f'<script type="module">{js_code.replace("</script>", "<\\/script>")}</script></body>')
        return final_html
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3>"

# --- TAMPILKAN HEADER & SIDEBAR PREMIUM (DI ATAS) ---
if 'result' not in st.session_state:
    st.session_state.result = None

# 1. Tampilkan Dashboard (Hanya Header, Sidebar, dan Hasil)
premium_html = get_premium_ui(st.session_state.result)
components.html(premium_html, height=1100)

# 2. Sisipkan Elemen Interaktif (PAS DI POSISI KOTAK KETIK DESAIN)
# Kita taruh di container agar posisinya pas
st.markdown("<div style='margin-top: -720px; padding: 0 420px;'>", unsafe_allow_html=True)
user_text = st.text_area("input", placeholder="Ekspresikan perasaan Anda di sini...", height=200)
if st.button("✨ Analisis Kondisi Emosi"):
    if user_text.strip():
        with st.spinner("Brain AI menganalisis..."):
            st.session_state.result = analyze_emotion(user_text)
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
