import streamlit as st
import os
import re
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# 1. Konfigurasi Halaman (Mewah & Bersih)
st.set_page_config(page_title="EmosiKu - AI Assistant", layout="wide", initial_sidebar_state="expanded")

# --- CSS TOTAL (Mereplikasi Desain Premium React ke Native Streamlit) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Clash+Display:wght@400;500;600;700&display=swap');
    
    /* Background & Font */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%) !important;
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Header Streamlit Bersih */
    header { visibility: hidden; }
    .block-container { padding-top: 2rem !important; }

    /* SIDEBAR MEWAH (Putih Bersih) */
    [data-testid="stSidebar"] {
        background-color: white !important;
        border-right: 1px solid #e2e8f0 !important;
        padding-top: 2rem;
    }
    
    /* JUDUL UTAMA (Clash Display) */
    .title-text {
        font-family: 'Clash Display', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 2rem;
    }

    /* KOTAK KACA (GLASSMORPHISM) */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 30px;
        padding: 2.5rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }

    /* INPUT AREA PREMIUM */
    .stTextArea textarea {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 20px !important;
        padding: 1.5rem !important;
        font-size: 1.1rem !important;
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    }

    /* TOMBOL UNGU PREMIUM (IDENTIK DENGAN REACT) */
    .stButton button {
        background: linear-gradient(90deg, #7c3aed 0%, #0891b2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        padding: 1rem 3rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        max-width: 400px;
    }
    
    .stButton button:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 15px 45px rgba(124, 58, 237, 0.5) !important;
    }

    /* HASIL ANALISIS (MEWAH) */
    .result-container {
        background: white;
        border-radius: 25px;
        padding: 2.5rem;
        border-left: 8px solid #7c3aed;
        box-shadow: 0 10px 25px rgba(0,0,0,0.03);
        margin-top: 2rem;
    }
    
    .stat-box {
        background: #f8fafc;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
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
        "description": 'Pola emosi Anda memancarkan keseimbangan dan kejernihan pikiran. Pertahankan energi positif ini.' if is_stable 
                      else 'AI mendeteksi pola yang mengarah pada kecemasan. Sangat disarankan untuk berbagi beban pikiran Anda.',
        "wellness": int(probs[0] * 100),
        "stress": int(probs[1] * 100),
        "clarity": int(torch.max(probs) * 100),
        "energy": 85 if is_stable else 45
    }

# --- SIDEBAR MEWAH ---
with st.sidebar:
    st.markdown("<h2 style='font-family: Clash Display;'>🧠 EmosiKu</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748b;'>AI Mental Health Assistant</p>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📊 Statistik")
    st.write("Sesi hari ini: 12")
    st.write("Kesehatan: 85%")

# --- KONTEN UTAMA ---
st.markdown('<h1 class="title-text">Analisis Kesehatan Mental AI</h1>', unsafe_allow_html=True)

# Layout Utama
col_input, col_space, col_result = st.columns([1.5, 0.1, 1.5])

with col_input:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 💬 Konsultasi")
    user_text = st.text_area("input_text", label_visibility="collapsed", placeholder="Tuliskan perasaan atau pikiran Anda secara bebas di sini...", height=300)
    
    if st.button("✨ Analisis Kondisi Emosi"):
        if user_text.strip():
            with st.spinner("AI sedang memproses..."):
                st.session_state.final_res = analyze_emotion(user_text)
        else:
            st.warning("Mohon isi curhatan Anda.")
    st.markdown('</div>', unsafe_allow_html=True)

with col_result:
    if 'final_res' in st.session_state:
        res = st.session_state.final_res
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; align-items: center; gap: 1.5rem; margin-bottom: 2rem;">
                <span style="font-size: 4rem;">{'😊' if res['sentiment'] == 'positive' else '😔'}</span>
                <div>
                    <h2 style="margin: 0; font-size: 2rem;">{res['status']}</h2>
                    <p style="margin: 0; color: #8b5cf6; font-weight: 700;">Keyakinan AI: {res['clarity']}%</p>
                </div>
            </div>
            <p style="font-size: 1.2rem; line-height: 1.6; color: #475569;">{res['description']}</p>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 2rem;">
                <div class="stat-box"><h3 style="color:#10b981; margin:0;">{res['wellness']}%</h3><small>Wellness</small></div>
                <div class="stat-box"><h3 style="color:#8b5cf6; margin:0;">{100 - res['stress']}%</h3><small>Ketenangan</small></div>
                <div class="stat-box"><h3 style="color:#06b6d4; margin:0;">{res['clarity']}%</h3><small>Kejelasan</small></div>
                <div class="stat-box"><h3 style="color:#f59e0b; margin:0;">{res['energy']}%</h3><small>Energi</small></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; min-height: 400px; text-align: center; opacity: 0.6;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">✨</div>
            <h3>Siap Mendengarkan</h3>
            <p>Hasil analisis emosi Anda akan muncul di sini.</p>
        </div>
        """, unsafe_allow_html=True)
