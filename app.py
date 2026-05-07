import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

@st.cache_resource
def load_ai_engine():
    MODEL_NAME = "indobenchmark/indobert-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

def clean_text(text, stopword_remover):
    text = re.sub(r'http\S+|[^a-zA-Z\s]', '', str(text)).lower()
    return stopword_remover.remove(text).strip()

def analyze_emotion(text):
    tokenizer, model, stopword_remover = load_ai_engine()
    cleaned = clean_text(text, stopword_remover)
    inputs = tokenizer(cleaned, return_tensors="pt", truncation=True, padding=True, max_length=128)
    
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
    dist_path = "frontend/dist"
    index_path = os.path.join(dist_path, "index.html")
    assets_path = os.path.join(dist_path, "assets")
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    js_files = [f for f in os.listdir(assets_path) if f.endswith(".js")]
    css_files = [f for f in os.listdir(assets_path) if f.endswith(".css")]
    
    with open(os.path.join(assets_path, js_files[0]), "r", encoding="utf-8") as f:
        js_code = f.read()
    with open(os.path.join(assets_path, css_files[0]), "r", encoding="utf-8") as f:
        css_code = f.read()
    
    # Suntikkan Hasil (jika ada) ke dalam variabel global JavaScript
    result_json = json.dumps(result) if result else "null"
    injection = f'<script>window.initialResult = {result_json};</script>'
    
    final_html = html_content.replace('<head>', f'<head>{injection}')
    final_html = final_html.replace('</head>', f'<style>{css_code}</style></head>')
    final_html = final_html.replace('</body>', f'<script type="module">{js_code.replace("</script>", "<\\/script>")}</script></body>')
    return final_html

# Inisialisasi State
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Render Utama
premium_html = get_premium_ui(st.session_state.last_result)
# Reset result setelah dirender agar tidak berulang
st.session_state.last_result = None

# Tangkap input dari React
component_value = components.html(premium_html, height=1200, scrolling=True)

# Proses Analisis
if component_value and isinstance(component_value, dict) and component_value.get('action') == 'analyze':
    with st.spinner("Menganalisis..."):
        st.session_state.last_result = analyze_emotion(component_value.get('text'))
        st.rerun()
