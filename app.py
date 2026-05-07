import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import subprocess
import time

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# --- BAGIAN 1: LOGIKA AI (Sama dengan api.py) ---
@st.cache_resource
def load_nlp_model():
    model_name = "indobenchmark/indobert-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

tokenizer, model, stopword_remover = load_nlp_model()

def clean_text(text):
    if not isinstance(text, str): return ""
    text = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|[^a-zA-Z\s]', '', text, flags=re.MULTILINE).lower()
    return re.sub(r'\s+', ' ', stopword_remover.remove(text)).strip()

# --- BAGIAN 2: JALANKAN API BACKEND SECARA OTOMATIS ---
# Kita tetap butuh api.py berjalan di background agar React bisa memanggilnya
if 'api_process' not in st.session_state:
    st.session_state.api_process = subprocess.Popen(["python", "api.py"])
    time.sleep(2) # Tunggu API siap

# --- BAGIAN 3: SERVE TAMPILAN PREMIUM ---
def get_premium_ui():
    dist_path = "frontend/dist"
    index_path = os.path.join(dist_path, "index.html")
    
    if not os.path.exists(index_path):
        return "<h3>Error: Frontend belum di-build. Jalankan 'npm run build' di folder frontend.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Cari nama file JS dan CSS di assets
    js_match = re.search(r'src="\./assets/(index-.*?\.js)"', html_content)
    css_match = re.search(r'href="\./assets/(index-.*?\.css)"', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        with open(os.path.join(dist_path, "assets", js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(dist_path, "assets", css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Ganti tag script dan link dengan kode aslinya (Inlining)
        html_content = re.sub(r'<script type="module" crossorigin src="\./assets/index-.*?\.js"></script>', 
                              f'<script type="module">{js_code}</script>', html_content)
        html_content = re.sub(r'<link rel="stylesheet" crossorigin href="\./assets/index-.*?\.css">', 
                              f'<style>{css_code}</style>', html_content)
    
    return html_content

# Tampilkan UI Premium
st.markdown("""
    <style>
        .stMain { padding: 0 !important; }
        iframe { border: none !important; }
    </style>
""", unsafe_allow_html=True)

premium_html = get_premium_ui()
components.html(premium_html, height=1000, scrolling=True)
