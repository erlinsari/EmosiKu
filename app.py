import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
import base64
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
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

def predict_emotion(text):
    # Cleaning
    text_clean = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|[^a-zA-Z\s]', '', text).lower()
    text_clean = stopword_remover.remove(text_clean)
    
    # Prediction
    inputs = tokenizer(text_clean, return_tensors="pt", truncation=True, max_length=128)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        prediction = torch.argmax(probs, dim=-1).item()
        conf = torch.max(probs).item()
    
    is_stable = prediction == 0
    return {
        "id": str(int(time.time())),
        "status": "Kondisi Stabil" if is_stable else "Terindikasi Gangguan",
        "sentiment": "positive" if is_stable else "negative",
        "description": "Pola emosi Anda memancarkan keseimbangan dan energi positif. Tidak terdeteksi indikasi gangguan mental yang signifikan." if is_stable else "AI kami mendeteksi pola dalam bahasa Anda yang mungkin mengindikasikan kecemasan atau beban emosional yang berat.",
        "wellness": int(probs[0][0].item() * 100),
        "stress": int(probs[0][1].item() * 100),
        "clarity": int(conf * 100),
        "energy": 85 if is_stable else 45,
        "lastInput": text
    }

# --- BAGIAN 2: SERVE TAMPILAN PREMIUM ---
def get_premium_ui_html():
    dist_path = "frontend/dist"
    index_path = os.path.join(dist_path, "index.html")
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    js_match = re.search(r'src="\./assets/(index-.*?\.js)"', html_content)
    css_match = re.search(r'href="\./assets/(index-.*?\.css)"', html_content)
    
    if js_match and css_match:
        with open(os.path.join(dist_path, "assets", js_match.group(1)), "rb") as f:
            js_base64 = base64.b64encode(f.read()).decode()
        with open(os.path.join(dist_path, "assets", css_match.group(1)), "rb") as f:
            css_base64 = base64.b64encode(f.read()).decode()
            
        html_content = html_content.replace(js_match.group(0), f'src="data:text/javascript;base64,{js_base64}"')
        html_content = html_content.replace(css_match.group(0), f'href="data:text/css;base64,{css_base64}"')
    
    return html_content

# Deklarasi Komponen
if "result" not in st.session_state:
    st.session_state.result = {"status": "Menunggu Analisis"}

# Tampilkan UI
st.markdown("""<style>.stApp { margin: 0; padding: 0; } iframe { border: none !important; width: 100%; }</style>""", unsafe_allow_html=True)

# Gunakan declare_component untuk komunikasi 2 arah
component_func = components.declare_component("emosiku_ui", html=get_premium_ui_html())
event_data = component_func(result=st.session_state.result)

# Proses jika ada data dari React
if event_data and event_data.get("action") == "analyze":
    text = event_data.get("text")
    if text:
        with st.spinner("AI sedang berpikir..."):
            st.session_state.result = predict_emotion(text)
            st.rerun()
