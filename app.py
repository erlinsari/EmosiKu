import streamlit as st
import streamlit.components.v1 as components
import os
import json
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
    assets_path = "frontend/dist/assets"
    
    if not os.path.exists(assets_path):
        return "<h3 style='color:white;'>Error: Folder assets tidak ditemukan. Harap jalankan build.</h3>"
    
    # Cari file JS dan CSS terbaru
    js_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".css")), None)
    
    if js_file and css_file:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Gunakan json.dumps untuk keamanan karakter spesial
        js_json = json.dumps(js_code)
        css_json = json.dumps(css_code)
        
        final_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <style>
                html, body, #root {{ height: 100%; margin: 0; padding: 0; background: #ffffff; }}
            </style>
            <script>
                (function() {{
                    const cssCode = {css_json};
                    const cssBlob = new Blob([cssCode], {{ type: 'text/css' }});
                    const cssUrl = URL.createObjectURL(cssBlob);
                    const link = document.createElement('link');
                    link.rel = 'stylesheet';
                    link.href = cssUrl;
                    document.head.appendChild(link);

                    const jsCode = {js_json};
                    const jsBlob = new Blob([jsCode], {{ type: 'text/javascript' }});
                    const jsUrl = URL.createObjectURL(jsBlob);
                    
                    const script = document.createElement('script');
                    script.type = 'module';
                    script.src = jsUrl;
                    document.head.appendChild(script);
                }})();
            </script>
        </head>
        <body>
            <div id="root"></div>
        </body>
        </html>
        """
        return final_html
    
    return "<h3 style='color:white;'>Error: Gagal mendeteksi file index di folder assets.</h3>"

# Tampilkan UI
st.markdown("""
    <style>
        .stApp {{ background: #0f172a; margin: 0; padding: 0; }}
        iframe {{ border: none !important; width: 100%; min-height: 100vh; }}
        header {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

premium_html = get_premium_ui()
components.html(premium_html, height=1500, scrolling=True)
