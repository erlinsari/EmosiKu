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
    try:
        st.session_state.api_process = subprocess.Popen(["python", "api.py"])
    except:
        pass # Fallback jika python tidak ditemukan (biasanya python3 di linux)
    time.sleep(3)

# --- BAGIAN 3: SERVE TAMPILAN PREMIUM ---
def get_premium_ui():
    dist_path = "frontend/dist"
    index_path = os.path.join(dist_path, "index.html")
    
    if not os.path.exists(index_path):
        return "<h3 style='color: white;'>Error: Folder dist tidak ditemukan. Harap jalankan build.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Mencari file JS dan CSS dengan regex yang lebih fleksibel
    js_match = re.search(r'<script .*?src="\./assets/(index-.*?\.js)".*?></script>', html_content)
    css_match = re.search(r'<link .*?href="\./assets/(index-.*?\.css)".*?>', html_content)
    
    if js_match and css_match:
        js_tag = js_match.group(0)
        js_file = js_match.group(1)
        css_tag = css_match.group(0)
        css_file = css_match.group(1)
        
        with open(os.path.join(dist_path, "assets", js_file), "r", encoding="utf-8") as f:
            js_code = f.read().replace('</script>', '<\/script>') # Escape script tag
        with open(os.path.join(dist_path, "assets", css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Injeksi dengan metode yang lebih aman
        new_js = f'<script type="module">\n{js_code}\n</script>'
        new_css = f'<style>\n{css_code}\n</style>'
        
        html_content = html_content.replace(js_tag, new_js)
        html_content = html_content.replace(css_tag, new_css)
    else:
        return "<h3 style='color: white;'>Error: Gagal mendeteksi aset di index.html.</h3>"
    
    return html_content

# Tampilkan UI
st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; }
        header { display: none !important; }
        .stMain { padding: 0 !important; }
    </style>
""", unsafe_allow_html=True)

with st.spinner("Memuat Tampilan EmosiKu..."):
    premium_html = get_premium_ui()
    components.html(premium_html, height=1200, scrolling=True)
