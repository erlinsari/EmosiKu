import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman Mewah
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="collapsed")

# --- SUNTIKAN CSS MEWAH (Mempercantik Elemen Asli Agar Senada dengan React) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .block-container { padding: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: #f8fafc !important; }
    
    /* Percantik TextArea agar Glassmorphism */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        font-family: 'Outfit', sans-serif !important;
        color: #1e293b !important;
    }
    
    /* Percantik Tombol agar Mewah (Ungu-Biru) */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed 0%, #0891b2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        font-family: 'Outfit', sans-serif !important;
        box-shadow: 0 10px 30px rgba(139,92,246,0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        max-width: 350px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 45px rgba(139,92,246,0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

@st.cache_resource
def load_ai_engine():
    # Model Terlatih (IndoRoBERTa)
    MODEL_NAME = "w11wo/indonesian-roberta-base-sentiment-classifier"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

def analyze_emotion(text):
    tokenizer, model, stopword_remover = load_ai_engine()
    text_clean = re.sub(r'http\S+|[^a-zA-Z\s]', '', str(text)).lower()
    inputs = tokenizer(text_clean, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    pred = torch.argmax(probs).item()
    confidence = int(probs[pred] * 100)
    
    # 0: negative, 1: neutral, 2: positive
    if pred == 2:
        status, sentiment = "Kondisi Sangat Stabil", "positive"
        desc = "Luar biasa! Energi positif Anda sangat kuat. Pikiran Anda jernih dan penuh dengan kebahagiaan."
        w, s, e = 95, 5, 90
    elif pred == 1:
        status, sentiment = "Kondisi Stabil", "positive"
        desc = "Kondisi emosi Anda terpantau seimbang dan tenang. Anda memiliki kontrol yang baik atas pikiran Anda."
        w, s, e = 75, 15, 70
    else:
        status, sentiment = "Terindikasi Gangguan Psikologis", "negative"
        desc = "AI mendeteksi adanya tekanan emosional atau kesedihan yang mendalam. Sangat disarankan untuk beristirahat atau berbicara dengan seseorang."
        w, s, e = 30, 80, 40

    return {
        "status": status, "sentiment": sentiment, "description": desc,
        "wellness": w, "stress": s, "clarity": confidence, "energy": e,
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

# --- TAMPILKAN HEADER & SIDEBAR PREMIUM ---
if 'res' not in st.session_state:
    st.session_state.res = None

# 1. Tampilkan Bagian Atas Dashboard (Sidebar & Header)
premium_html = get_premium_ui(st.session_state.res)
components.html(premium_html, height=450) # Tinggi pas untuk Header saja

# 2. Sisipkan Elemen Interaktif Asli (PASTI BISA DIKLIK)
st.markdown("<div style='padding: 0 420px; margin-top: -150px;'>", unsafe_allow_html=True)
user_text = st.text_area("input", placeholder="Ekspresikan perasaan Anda di sini...", height=200, label_visibility="collapsed")
if st.button("✨ Analisis Kondisi Emosi"):
    if user_text.strip():
        with st.spinner("AI sedang menganalisis..."):
            st.session_state.res = analyze_emotion(user_text)
            st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# 3. Tampilkan Hasil (Jika Ada) di Bawah
if st.session_state.res:
    # Render ulang UI dengan hasil
    premium_html_with_res = get_premium_ui(st.session_state.res)
    components.html(premium_html_with_res, height=1100)
