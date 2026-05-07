import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# 1. Deklarasikan Jalur Dua Arah (Custom Component)
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend/dist")
# Gunakan declare_component agar React bisa mengirim balik data ke Python
render_emosiku = components.declare_component("emosiku", path=build_dir)

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

# Logika Utama
if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Tampilkan Komponen (Sekarang sudah Dua Arah)
# Kita kirim hasil terakhir sebagai "result" ke React
data_from_react = render_emosiku(result=st.session_state.last_result, key="emosiku_main")

# Jika ada data masuk dari React (artinya tombol diklik)
if data_from_react and data_from_react.get('action') == 'analyze':
    text_to_analyze = data_from_react.get('text')
    if text_to_analyze:
        with st.spinner("Sedang menganalisis emosi Anda..."):
            st.session_state.last_result = analyze_emotion(text_to_analyze)
            st.rerun()
