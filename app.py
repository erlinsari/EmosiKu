import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman (Tanpa Margin)
st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide", initial_sidebar_state="collapsed")

# CSS untuk mematikan padding Streamlit agar dashboard memenuhi layar
st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    iframe { border: none !important; }
</style>
""", unsafe_allow_html=True)

# 2. Deklarasi Komponen (Jalur Absolut)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(BASE_DIR, "frontend", "dist")

# Pastikan folder build ada
if not os.path.exists(os.path.join(BUILD_DIR, "index.html")):
    st.error(f"FATAL: Folder 'dist' tidak ditemukan di {BUILD_DIR}. Pastikan Anda sudah menjalankan 'npm run build'.")
    st.stop()

# Aktifkan Jalur Dua Arah (Resmi)
render_emosiku = components.declare_component("emosiku", path=BUILD_DIR)

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

if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# 3. Jalankan Dashboard (React Asli)
# Kirim hasil terakhir ke React via props
data_from_react = render_emosiku(result=st.session_state.last_result, key="emosiku_final")

# 4. Tangkap Sinyal Analisis dari Tombol React
if data_from_react and data_from_react.get('action') == 'analyze':
    with st.spinner("AI sedang menganalisis..."):
        st.session_state.last_result = analyze_emotion(data_from_react.get('text'))
        st.rerun()
