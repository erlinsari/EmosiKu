import streamlit as st
import streamlit.components.v1 as components
import os
import re
import torch
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
    text_clean = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|[^a-zA-Z\s]', '', text).lower()
    text_clean = stopword_remover.remove(text_clean)
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

# --- BAGIAN 2: DEKLARASI KOMPONEN ---
# Menggunakan path absolut agar server Cloud tidak bingung
parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "frontend", "dist")

if not os.path.exists(build_dir):
    st.error(f"Folder build tidak ditemukan di: {build_dir}")
else:
    # Nama komponen baru untuk memaksa refresh cache
    emosiku_ui = components.declare_component("emosiku_premium_v1", path=build_dir)

    if "result" not in st.session_state:
        st.session_state.result = {"status": "Menunggu Analisis"}

    st.markdown("""<style>.stApp { margin: 0; padding: 0; } iframe { border: none !important; width: 100%; height: 100vh; }</style>""", unsafe_allow_html=True)

    # Jalankan komponen
    event_data = emosiku_ui(result=st.session_state.result)

    # Logika Analisis
    if event_data and event_data.get("action") == "analyze":
        text = event_data.get("text")
        if text:
            with st.spinner("AI sedang menganalisis..."):
                st.session_state.result = predict_emotion(text)
                st.rerun()
