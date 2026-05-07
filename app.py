import streamlit as st
import streamlit.components.v1 as components
import os
import re
import base64
import torch
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

# --- BAGIAN 3: SERVE TAMPILAN PREMIUM ---
def get_premium_ui():
    dist_path = "frontend/dist"
    index_path = os.path.join(dist_path, "index.html")
    
    if not os.path.exists(index_path):
        return "<h3>Error: Folder dist tidak ditemukan.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Deteksi file JS dan CSS
    js_match = re.search(r'src="\./assets/(index-.*?\.js)"', html_content)
    css_match = re.search(r'href="\./assets/(index-.*?\.css)"', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        # Baca file asli
        with open(os.path.join(dist_path, "assets", js_file), "rb") as f:
            js_base64 = base64.b64encode(f.read()).decode()
        with open(os.path.join(dist_path, "assets", css_file), "rb") as f:
            css_base64 = base64.b64encode(f.read()).decode()
            
        # Konstruksi HTML baru yang bersih
        # Kita hapus tag asli dan buat tag baru di bagian head
        final_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>EmosiKu</title>
            <style>
                html, body, #root {{ height: 100%; margin: 0; padding: 0; background: #f8fafc; }}
            </style>
            <style type="text/css">
                /* CSS Terinjeksi */
                {base64.b64decode(css_base64).decode('utf-8', errors='ignore')}
            </style>
        </head>
        <body>
            <div id="root"></div>
            <script type="module">
                /* JS Terinjeksi */
                {base64.b64decode(js_base64).decode('utf-8', errors='ignore')}
            </script>
        </body>
        </html>
        """
        return final_html
    
    return "<h3>Error: Gagal memetakan aset.</h3>"

# Tampilkan UI
st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; }
        header { display: none !important; }
        footer { display: none !important; }
    </style>
""", unsafe_allow_html=True)

premium_html = get_premium_ui()
components.html(premium_html, height=1500, scrolling=True)
