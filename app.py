import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman (Hapus Margin & Ruang Hitam)
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="collapsed")

# Suntikan CSS agar dashboard memenuhi layar
st.markdown("""
<style>
    .block-container { padding: 4rem 0 0 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: white !important; }
    iframe { border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

@st.cache_resource
def load_ai_engine():
    # MENGGUNAKAN MODEL YANG SUDAH TERLATIH (FINE-TUNED) UNTUK SENTIMEN INDONESIA
    # Model ini jauh lebih akurat untuk mendeteksi emosi bahagia/sedih
    MODEL_NAME = "w11wo/indonesian-roberta-base-sentiment-classifier"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

def analyze_emotion(text):
    tokenizer, model, stopword_remover = load_ai_engine()
    
    # Preprocessing ringan
    text_clean = re.sub(r'http\S+|[^a-zA-Z\s]', '', str(text)).lower()
    
    # Tokenisasi
    inputs = tokenizer(text_clean, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Model w11wo memiliki 3 label: 0: negative, 1: neutral, 2: positive
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    pred = torch.argmax(probs).item()
    
    # Pemetaan Emosi ke Status Kesehatan Mental
    # Label 2 (Positive) & 1 (Neutral) -> Stabil
    # Label 0 (Negative) -> Terindikasi Gangguan
    is_stable = pred != 0 
    confidence = int(probs[pred] * 100)
    
    if pred == 2: # Positive
        status = "Kondisi Sangat Stabil"
        desc = "Luar biasa! Energi positif Anda sangat kuat. Pikiran Anda jernih dan penuh dengan kebahagiaan."
        sentiment = "positive"
        wellness, stress, energy = 95, 5, 90
    elif pred == 1: # Neutral
        status = "Kondisi Stabil"
        desc = "Kondisi emosi Anda terpantau seimbang dan tenang. Anda memiliki kontrol yang baik atas pikiran Anda."
        sentiment = "positive"
        wellness, stress, energy = 75, 15, 70
    else: # Negative
        status = "Terindikasi Gangguan Psikologis"
        desc = "AI mendeteksi adanya tekanan emosional atau kesedihan yang mendalam. Sangat disarankan untuk beristirahat atau berbicara dengan seseorang yang Anda percayai."
        sentiment = "negative"
        wellness, stress, energy = 30, 80, 40

    return {
        "status": status,
        "sentiment": sentiment,
        "description": desc,
        "wellness": wellness,
        "stress": stress,
        "clarity": confidence,
        "energy": energy,
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
        return f"<h3>Error loading UI: {str(e)}</h3>"

# --- PENERIMA ANALISIS ---
query_params = st.query_params
if "analyze" in query_params:
    text_to_analyze = query_params["analyze"]
    st.query_params.clear()
    with st.spinner("🧠 AI sedang menganalisis perasaan Anda..."):
        st.session_state.current_result = analyze_emotion(text_to_analyze)
        st.rerun()

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# --- TAMPILKAN DASHBOARD ---
premium_html = get_premium_ui(st.session_state.current_result)
st.session_state.current_result = None

components.html(premium_html, height=1500, scrolling=True)
