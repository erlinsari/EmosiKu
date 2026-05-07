import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman (Hapus Margin & Ruang Hitam)
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="collapsed")

# Suntikan CSS agar dashboard memenuhi layar
st.markdown("""
<style>
    .block-container { padding: 0 !important; max-width: 100% !important; }
    [data-testid="stAppViewContainer"] { background: white !important; }
    iframe { border: none !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "dist")

# JEMBATAN RESMI STREAMLIT
if not os.path.exists(DIST_DIR):
    st.error(f"Folder build tidak ditemukan di: {DIST_DIR}. Harap jalankan 'npm run build' terlebih dahulu.")
    st.stop()

# Deklarasikan komponen desain mewah Anda
emosiku_dashboard = components.declare_component("emosiku_dashboard", path=DIST_DIR)

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

# --- LOGIKA APLIKASI ---
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Tampilkan Dashboard Mewah & Tangkap Sinyal dari Tombol
# Argumen 'result' dikirim balik ke React untuk ditampilkan di panel
value = emosiku_dashboard(result=st.session_state.last_result, key="dashboard")

# Jika tombol di React diklik, 'value' akan berisi data teks
if value and value.get('action') == 'analyze':
    text_to_process = value.get('text', '')
    if text_to_process:
        # Jalankan IndoBERT
        st.session_state.last_result = analyze_emotion(text_to_process)
        # Rerun agar dashboard terupdate dengan hasil baru
        st.rerun()
