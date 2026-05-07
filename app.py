import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman (Berikan Ruang di Atas agar Tidak Terpotong)
st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide", initial_sidebar_state="collapsed")

# Suntikan CSS dengan Padding Atas yang Cukup
st.markdown("""
<style>
    /* Berikan jarak 4rem di atas agar tidak terpotong header */
    .block-container { padding: 4rem 1rem 1rem 1rem !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: #f8fafc !important; }
    iframe { border: none !important; width: 100% !important; border-radius: 20px; }
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
        # Gunakan window.top untuk memastikan sinyal sampai ke jendela utama
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

# --- PENERIMA ANALISIS ---
query_params = st.query_params
if "analyze" in query_params:
    text_to_analyze = query_params["analyze"]
    st.query_params.clear()
    with st.spinner("AI sedang menganalisis perasaan Anda..."):
        st.session_state.current_result = analyze_emotion(text_to_analyze)
        st.rerun()

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# --- TAMPILKAN DASHBOARD ---
premium_html = get_premium_ui(st.session_state.current_result)
st.session_state.current_result = None

components.html(premium_html, height=1200, scrolling=True)
