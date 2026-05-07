import streamlit as st
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Konfigurasi Halaman
st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide", initial_sidebar_state="collapsed")

# --- CSS MEWAH (Suntikan Desain Premium) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Clash+Display:wght@400;500;600;700&display=swap');
    
    .main { background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%); }
    
    /* Container Utama */
    .premium-container {
        padding: 2rem;
        font-family: 'Outfit', sans-serif;
    }
    
    .title-text {
        font-family: 'Clash Display', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    /* Kotak Input Custom */
    .stTextArea textarea {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #8b5cf6 !important;
        box-shadow: 0 0 25px rgba(139, 92, 246, 0.2) !important;
    }
    
    /* Tombol Premium */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed 0%, #0891b2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 0.8rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 40px rgba(124, 58, 237, 0.5) !important;
    }
    
    /* Panel Hasil (Glassmorphism) */
    .result-panel {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 30px;
        padding: 2.5rem;
        margin-top: 2rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.05);
    }
    
    .stat-card {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.02);
        border: 1px solid #f1f5f9;
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
        "status": 'Kondisi Stabil' if is_stable else 'Terindikasi Gangguan Psikologis',
        "sentiment": 'positive' if is_stable else 'negative',
        "description": 'Pola emosi Anda memancarkan keseimbangan dan energi positif. Pertahankan kesehatan mental Anda.' if is_stable 
                      else 'AI mendeteksi pola yang mengindikasikan kecemasan atau beban emosional. Sangat disarankan untuk berbagi perasaan ini.',
        "wellness": int(probs[0] * 100),
        "stress": int(probs[1] * 100),
        "clarity": int(torch.max(probs) * 100),
        "energy": 85 if is_stable else 45
    }

# --- TAMPILAN UTAMA ---
st.markdown('<div class="premium-container">', unsafe_allow_html=True)
st.markdown('<h1 class="title-text">Analisis Kesehatan Mental AI</h1>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    user_input = st.text_area("💬 Konsultasi", placeholder="Ekspresikan perasaan atau pikiran Anda secara bebas di sini...", height=250)
    btn_analyze = st.button("✨ Analisis Kondisi Emosi")

if btn_analyze and user_input.strip():
    with st.spinner("🧠 AI sedang memproses..."):
        result = analyze_emotion(user_input)
        
        # Tampilkan Hasil dengan Gaya Premium
        st.markdown(f"""
        <div class="result-panel">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
                <span style="font-size: 3rem;">{'😊' if result['sentiment'] == 'positive' else '😔'}</span>
                <div>
                    <h2 style="margin: 0; color: #1e293b;">{result['status']}</h2>
                    <p style="margin: 0; color: #64748b;">Keyakinan AI: {result['clarity']}%</p>
                </div>
            </div>
            <p style="font-size: 1.2rem; line-height: 1.6; color: #475569;">{result['description']}</p>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 2rem;">
                <div class="stat-card">
                    <h4 style="margin:0; color:#10b981;">{result['wellness']}%</h4>
                    <small>Wellness</small>
                </div>
                <div class="stat-card">
                    <h4 style="margin:0; color:#8b5cf6;">{100 - result['stress']}%</h4>
                    <small>Ketenangan</small>
                </div>
                <div class="stat-card">
                    <h4 style="margin:0; color:#06b6d4;">{result['clarity']}%</h4>
                    <small>Kejelasan</small>
                </div>
                <div class="stat-card">
                    <h4 style="margin:0; color:#f59e0b;">{result['energy']}%</h4>
                    <small>Energi</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
elif btn_analyze:
    st.warning("Silakan tuliskan sesuatu terlebih dahulu.")

st.markdown('</div>', unsafe_allow_html=True)
