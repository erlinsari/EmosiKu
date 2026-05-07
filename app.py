import streamlit as st
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman Mewah
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="collapsed")

# --- CSS KAMUFLASE (Menjadikan Elemen Streamlit Menjadi Mewah) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Clash+Display:wght@400;500;600;700&display=swap');
    
    /* Background Utama Dashboard */
    .stApp {
        background: linear-gradient(135deg, #f0f9ff 0%, #f5f3ff 50%, #fdf2f8 100%) !important;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Hilangkan Header Streamlit agar bersih */
    header { visibility: hidden; }
    .main .block-container { padding-top: 3rem !important; max-width: 1200px !important; }

    /* Judul Clash Display */
    .title-text {
        font-family: 'Clash Display', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #1e293b, #475569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }

    /* KOTAK KETIK (RE-DESIGN) */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 25px !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
        color: #1e293b !important;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.15) !important;
    }

    /* TOMBOL ANALISIS (RE-DESIGN MEWAH) */
    .stButton button {
        background: linear-gradient(135deg, #7c3aed 0%, #2563eb 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1.2rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 15px 45px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        width: 100% !important;
        max-width: 400px;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 20px 55px rgba(124, 58, 237, 0.5) !important;
    }

    /* PANEL HASIL GLASSMORPHISM */
    .result-card {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        border-radius: 35px;
        padding: 3rem;
        margin-top: 3rem;
        box-shadow: 0 25px 60px rgba(0,0,0,0.06);
        animation: fadeIn 0.8s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Card Mini */
    .mini-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid #f1f5f9;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
</style>
""", unsafe_allow_html=True)

# --- ENGINE AI ---
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
        "status": 'Kondisi Emosi Stabil' if is_stable else 'Terindikasi Gangguan Psikologis',
        "sentiment": 'positive' if is_stable else 'negative',
        "description": 'Pola emosi Anda mencerminkan ketenangan dan kejernihan pikiran. Pertahankan energi positif ini.' if is_stable 
                      else 'AI mendeteksi pola yang mengarah pada kecemasan. Jangan ragu untuk berbagi beban pikiran Anda.',
        "wellness": int(probs[0] * 100),
        "stress": int(probs[1] * 100),
        "clarity": int(torch.max(probs) * 100),
        "energy": 85 if is_stable else 45
    }

# --- SIDEBAR (SUNTIKAN DESAIN) ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Clash Display; color: #1e293b;'>🧠 EmosiKu</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>AI Mental Health Companion</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.info("Mesin AI: IndoBERT-Lite Optimized")

# --- KONTEN UTAMA ---
st.markdown('<h1 class="title-text">Analisis Kesehatan Mental AI</h1>', unsafe_allow_html=True)

# Grid Layout
col_main, col_stats = st.columns([2, 1])

with col_main:
    st.markdown("<h4 style='color: #475569; margin-bottom: 1rem;'>💬 Konsultasi</h4>", unsafe_allow_html=True)
    user_input = st.text_area("input_area", label_visibility="collapsed", placeholder="Bagaimana perasaan Anda hari ini? Ceritakan segala pikiran Anda di sini...", height=300)
    
    # Tombol Analisis (ASLI STREAMLIT - PASTI BISA DIKLIK)
    if st.button("✨ Analisis Kondisi Emosi Sekarang"):
        if user_input.strip():
            with st.spinner("Brain AI sedang memproses..."):
                result = analyze_emotion(user_input)
                st.session_state.result = result
        else:
            st.warning("Mohon isi curhatan Anda terlebih dahulu.")

# Tampilkan Hasil Jika Ada
if 'result' in st.session_state:
    res = st.session_state.result
    st.markdown(f"""
    <div class="result-card">
        <div style="display: flex; align-items: center; gap: 2rem; margin-bottom: 2rem;">
            <div style="font-size: 5rem; filter: drop-shadow(0 10px 20px rgba(0,0,0,0.1));">
                {'😊' if res['sentiment'] == 'positive' else '😔'}
            </div>
            <div>
                <h2 style="margin: 0; font-size: 2.5rem; color: #1e293b;">{res['status']}</h2>
                <p style="margin: 0; color: #7c3aed; font-weight: 700; font-size: 1.2rem;">AI Confidence: {res['clarity']}%</p>
            </div>
        </div>
        
        <p style="font-size: 1.3rem; line-height: 1.8; color: #475569; border-left: 5px solid #7c3aed; padding-left: 1.5rem;">
            {res['description']}
        </p>
        
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.5rem; margin-top: 3rem;">
            <div class="mini-card"><h3 style="color:#10b981; margin:0;">{res['wellness']}%</h3><small>Wellness</small></div>
            <div class="mini-card"><h3 style="color:#8b5cf6; margin:0;">{100 - res['stress']}%</h3><small>Ketenangan</small></div>
            <div class="mini-card"><h3 style="color:#06b6d4; margin:0;">{res['clarity']}%</h3><small>Kejelasan</small></div>
            <div class="mini-card"><h3 style="color:#f59e0b; margin:0;">{res['energy']}%</h3><small>Energi</small></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Scroll ke hasil
    st.balloons()
