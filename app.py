import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import base64
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import subprocess
import time

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# --- BAGIAN 1: LOGIKA AI ---
@st.cache_resource
def load_nlp_model():
    model_name = "indobenchmark/indobert-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

tokenizer, model, stopword_remover = load_nlp_model()

# --- BAGIAN 2: JALANKAN API BACKEND ---
if 'api_process' not in st.session_state:
    st.session_state.api_process = subprocess.Popen(["python", "api.py"])
    time.sleep(3)

# --- BAGIAN 3: SERVE TAMPILAN PREMIUM (Metode Base64 Safe) ---
def get_premium_ui():
    dist_path = "frontend/dist"
    index_path = os.path.join(dist_path, "index.html")
    
    if not os.path.exists(index_path):
        return "<h3>Error: Folder dist tidak ditemukan.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Cari file JS dan CSS
    js_match = re.search(r'src="\./assets/(index-.*?\.js)"', html_content)
    css_match = re.search(r'href="\./assets/(index-.*?\.css)"', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        # Baca dan Encode ke Base64 agar aman dari karakter spesial
        with open(os.path.join(dist_path, "assets", js_file), "rb") as f:
            js_base64 = base64.b64encode(f.read()).decode()
        with open(os.path.join(dist_path, "assets", css_file), "rb") as f:
            css_base64 = base64.b64encode(f.read()).decode()
            
        # Ganti tag dengan Data URI (Teknik Paling Aman)
        html_content = re.sub(r'<script type="module" crossorigin src="\./assets/index-.*?\.js"></script>', 
                              f'<script type="module" src="data:text/javascript;base64,{js_base64}"></script>', html_content)
        html_content = re.sub(r'<link rel="stylesheet" crossorigin href="\./assets/index-.*?\.css">', 
                              f'<link rel="stylesheet" href="data:text/css;base64,{css_base64}">', html_content)
    
    return html_content

# Tampilkan UI
st.markdown("""
    <style>
        .stApp { margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

premium_html = get_premium_ui()
components.html(premium_html, height=1200, scrolling=True)
