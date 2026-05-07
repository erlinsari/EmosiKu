import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import time

# Page config
st.set_page_config(page_title="EmosiKu", layout="wide", initial_sidebar_state="collapsed")

# --- AI LOGIC ---
@st.cache_resource
def load_nlp():
    m = "indobenchmark/indobert-base-p1"
    tok = AutoTokenizer.from_pretrained(m)
    mod = AutoModelForSequenceClassification.from_pretrained(m, num_labels=2)
    sw = StopWordRemoverFactory().create_stop_word_remover()
    return tok, mod, sw

tokenizer, model, stopword_remover = load_nlp()

def get_prediction(text):
    clean = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    clean = stopword_remover.remove(clean)
    inputs = tokenizer(clean, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        out = model(**inputs)
        probs = torch.nn.functional.softmax(out.logits, dim=-1)
        pred = torch.argmax(probs, dim=-1).item()
        conf = torch.max(probs).item()
    is_s = pred == 0
    return {
        "id": str(int(time.time())),
        "status": "Kondisi Stabil" if is_s else "Terindikasi Gangguan",
        "sentiment": "positive" if is_s else "negative",
        "description": "Pola emosi Anda memancarkan energi positif." if is_s else "Terdeteksi beban emosional yang memerlukan perhatian.",
        "wellness": int(probs[0][0].item() * 100),
        "stress": int(probs[0][1].item() * 100),
        "clarity": int(conf * 100),
        "energy": 85 if is_s else 45,
        "lastInput": text
    }

# --- UI COMPONENT ---
# Menggunakan alamat lengkap agar server tidak tersesat
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "web")

if not os.path.exists(build_dir):
    st.error(f"Folder 'web' tidak ditemukan di: {build_dir}")
else:
    # Nama komponen baru untuk memaksa refresh total
    ui_component = components.declare_component("emosiku_premium_final_fixed", path=build_dir)

    if "result" not in st.session_state:
        st.session_state.result = {"status": "Menunggu Analisis"}

    # Full screen style
    st.markdown("""<style>
        .stApp { margin: 0; padding: 0; background: #f8fafc; }
        iframe { border: none !important; width: 100%; height: 100vh; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>""", unsafe_allow_html=True)

    # Render Component
    response = ui_component(result=st.session_state.result)

    # Handle Analysis Request
    if response and response.get("action") == "analyze":
        text = response.get("text")
        if text:
            st.session_state.result = get_prediction(text)
            st.rerun()
