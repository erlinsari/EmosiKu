import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

@st.cache_resource
def load_ai_engine():
    MODEL_NAME = "indobenchmark/indobert-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

def analyze_emotion(text):
    tokenizer, model, stopword_remover = load_ai_engine()
    text = re.sub(r'http\S+|[^a-zA-Z\s]', '', str(text)).lower()
    cleaned = stopword_remover.remove(text).strip()
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        out = model(**inputs)
    probs = torch.softmax(out.logits, dim=-1)[0]
    pred = torch.argmax(out.logits, dim=-1).item()
    is_stable = pred == 0
    return {
        "status": 'Kondisi Stabil' if is_stable else 'Terindikasi Gangguan Psikologis',
        "sentiment": 'positive' if is_stable else 'negative',
        "description": 'Pola emosi Anda memancarkan keseimbangan.' if is_stable 
                      else 'AI mendeteksi pola yang mengindikasikan kecemasan.',
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
        
        if not os.path.exists(index_path):
            return f"SYSTEM_ERROR: Desain tidak ditemukan."
        
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        js_files = [f for f in os.listdir(assets_dir) if f.endswith(".js")]
        css_files = [f for f in os.listdir(assets_dir) if f.endswith(".css")]
        
        if not js_files:
            return "SYSTEM_ERROR: JS tidak ditemukan."
            
        result_json = json.dumps(result) if result else "null"
        injection = f'<script>window.initialResult = {result_json};</script>'
        
        with open(os.path.join(assets_dir, js_files[0]), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_dir, css_files[0]), "r", encoding="utf-8") as f:
            css_code = f.read()
        
        final_html = html_content.replace('<head>', f'<head>{injection}')
        final_html = final_html.replace('</head>', f'<style>{css_code}</style></head>')
        final_html = final_html.replace('</body>', f'<script type="module">{js_code.replace("</script>", "<\\/script>")}</script></body>')
        
        return final_html
    except Exception as e:
        return f"SYSTEM_ERROR: {str(e)}"

# Logika URL Bridge
if "analyze" in st.query_params:
    text = st.query_params["analyze"]
    st.query_params.clear()
    with st.spinner("Menganalisis..."):
        st.session_state.current_result = analyze_emotion(text)
        st.rerun()

if 'current_result' not in st.session_state:
    st.session_state.current_result = None

# Render
premium_html = get_premium_ui(st.session_state.current_result)
st.session_state.current_result = None

if premium_html.startswith("SYSTEM_ERROR:"):
    st.error(premium_html)
else:
    components.html(premium_html, height=1200, scrolling=True)
