import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
import glob
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="collapsed")

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
    # Model RoBERTa Indonesia (Akurat & Cerdas)
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

# --- LOGIKA PENERIMA (SANGAT KRUSIAL) ---
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Ambil query parameter
q = st.query_params
if "analyze" in q:
    txt = q["analyze"]
    # JANGAN LANGSUNG CLEAR. Simpan dulu ke session state.
    st.session_state.last_result = analyze_emotion(txt)
    # Clear query param agar tidak looping, lalu rerun
    st.query_params.clear()
    st.rerun()

# Tampilkan UI
premium_html = get_premium_ui(st.session_state.last_result)
# Reset setelah UI dirender agar tidak muncul terus saat refresh biasa
# Tapi jangan langsung None di sini jika ingin persistent. 
# Kita biarkan saja, dia akan reset saat user klik tombol lagi.

components.html(premium_html, height=1500, scrolling=True)
