import streamlit as st
import streamlit.components.v1 as components
import torch
import re
import pandas as pd
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
import time

st.set_page_config(page_title="EmosiKu - Psychotherapy", layout="wide")

# 1. INJEKSI JAVASCRIPT UNTUK EFEK KURSOR AJAIB & PARTIKEL
components.html("""
<script>
const doc = window.parent.document;
if (!doc.getElementById("magic-cursor")) {
    const script = doc.createElement("script");
    script.id = "magic-cursor";
    script.innerHTML = `
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100vw';
        canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '9999';
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        
        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        const particles = [];
        window.addEventListener('mousemove', (e) => {
            if(Math.random() > 0.5) { // Kurangi jumlah partikel sedikit agar elegan
                particles.push({
                    x: e.clientX, y: e.clientY,
                    size: Math.random() * 5 + 3,
                    vx: Math.random() * 2 - 1, vy: Math.random() * 2 - 1,
                    life: 1,
                    // Warna bola memori: Kuning (Joy), Biru (Sadness), Oranye (Anxiety), Hijau (Disgust)
                    color: ['#fef08a', '#93c5fd', '#fdba74', '#bbf7d0'][Math.floor(Math.random() * 4)]
                });
            }
        });

        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for(let i=0; i<particles.length; i++) {
                let p = particles[i];
                ctx.globalAlpha = p.life;
                ctx.fillStyle = p.color;
                ctx.shadowBlur = 10;
                ctx.shadowColor = p.color;
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
                ctx.fill();
                p.x += p.vx; p.y += p.vy - 1; // Mengambang ke atas
                p.life -= 0.015;
                if(p.life <= 0) { particles.splice(i, 1); i--; }
            }
            requestAnimationFrame(render);
        }
        render();
    `;
    doc.body.appendChild(script);
}
</script>
""", height=0, width=0)

# Membaca file CSS eksternal (Sage Green Psychotherapy Theme)
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Elemen Bergerak Organik + GIF Karakter Inside Out di Background
st.markdown("""
<div class="organic-shape shape-1"></div>
<div class="organic-shape shape-2"></div>

<!-- Gaya Bingkai Polaroid untuk GIF agar terlihat elegan -->
<style>
.gif-frame {
    position: fixed; z-index: 0;
    border-radius: 15px; border: 5px solid rgba(255,255,255,0.8);
    box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    overflow: hidden; width: 220px;
    animation: floatOrganic 6s infinite alternate;
}
.gif-frame img { width: 100%; height: auto; display: block; }
</style>

<!-- Sadness - Pojok Kiri Bawah -->
<div class="gif-frame" style="bottom: 20px; left: 20px; animation-delay: 0s;">
    <img src="https://media.giphy.com/media/3o7aD2saal6gP54QhO/giphy.gif">
</div>

<!-- Disgust - Pojok Kanan Bawah -->
<div class="gif-frame" style="bottom: 20px; right: 20px; animation-delay: -2s;">
    <img src="https://media.giphy.com/media/13FrpeVH09Zrb2/giphy.gif">
</div>

<!-- Anger - Kanan Atas -->
<div class="gif-frame" style="top: 20px; right: 20px; animation-delay: -4s;">
    <img src="https://media.giphy.com/media/11tTNkNy1SdXGg/giphy.gif">
</div>

<!-- Fear - Kiri Atas -->
<div class="gif-frame" style="top: 20px; left: 20px; animation-delay: -1s;">
    <img src="https://media.giphy.com/media/ToMjGppLes0ENI5osOY/giphy.gif">
</div>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_model():
    model_path = "indobenchmark/indobert-base-p1" 
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, num_labels=2)
    return tokenizer, model

@st.cache_resource(show_spinner=False)
def load_stopword():
    return StopWordRemoverFactory().create_stop_word_remover()

tokenizer, model = load_model()
stopword = load_stopword()

def clean_text(text):
    if not isinstance(text, str): return ""
    text = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|[^a-zA-Z\s]', '', text, flags=re.MULTILINE).lower()
    return re.sub(r'\s+', ' ', stopword.remove(text)).strip()

def predict(text):
    inputs = tokenizer(clean_text(text), return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad(): out = model(**inputs)
    probs = torch.softmax(out.logits, dim=-1)[0]
    pred = torch.argmax(out.logits, dim=-1).item()
    return pred, probs[pred].item(), probs.numpy()

if 'history' not in st.session_state: st.session_state['history'] = []

# Judul Utama Berbasis Tipografi Elegan
st.markdown('''
<div class="title-container" style="position: relative; z-index: 1;">
    <div class="title-main">Emosi<i>Ku</i></div>
    <div class="subtitle">Sistem Deteksi Indikasi Gangguan Kesehatan Mental Berbasis NLP</div>
</div>
''', unsafe_allow_html=True)

col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown('<div class="metric-card" style="position: relative; z-index: 1;"><div class="card-header">Consultation text</div>', unsafe_allow_html=True)
    user_input = st.text_area("", height=220, placeholder="Ceritakan apa yang sedang Anda rasakan atau pikirkan hari ini. Ruang ini aman dan rahasia...", label_visibility="collapsed")
    
    if st.button("MULAI ANALISIS"):
        if user_input:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.markdown("<p style='color: #738a58; font-style: italic; font-weight: 600; font-family: Manrope;'>Menyelaraskan koneksi emosional...</p>", unsafe_allow_html=True)
            time.sleep(0.5)
            progress_bar.progress(30)
            
            status_text.markdown("<p style='color: #738a58; font-style: italic; font-weight: 600; font-family: Manrope;'>Menganalisis memori inti dari teks...</p>", unsafe_allow_html=True)
            time.sleep(0.5)
            progress_bar.progress(70)
            
            status_text.markdown("<p style='color: #738a58; font-style: italic; font-weight: 600; font-family: Manrope;'>Menyusun laporan diagnostik NLP...</p>", unsafe_allow_html=True)
            time.sleep(0.6)
            progress_bar.progress(100)
            status_text.empty()
            progress_bar.empty()
            
            pred, conf, probs = predict(user_input)
            st.session_state['history'].append({"Waktu": datetime.now().strftime("%H:%M:%S"), "Input": user_input[:40]+"...", "Status": "Terindikasi" if pred==1 else "Stabil", "Probabilitas": f"{conf:.2%}"})
            
            with col2:
                st.markdown('<div class="metric-card" style="position: relative; z-index: 1;">', unsafe_allow_html=True)
                st.markdown('<div class="card-header" style="border-bottom: 1px solid #c8d1bd; padding-bottom: 15px; margin-bottom: 25px;">Diagnostic results</div>', unsafe_allow_html=True)
                
                if pred == 1:
                    st.markdown('''
                    <div class="card-anxiety" style="display: flex; align-items: center; position: relative;">
                        <div style="flex: 1;">
                            <h2 class="result-title">Terindikasi Gangguan Psikologis</h2>
                            <p class="result-desc">Pola bahasa Anda menunjukkan indikasi kecemasan atau beban pikiran. Berbagi dengan profesional sangat disarankan.</p>
                        </div>
                        <img src="https://media.giphy.com/media/ToMjGppLes0ENI5osOY/giphy.gif" style="height: 140px; border-radius: 10px; margin-left: 15px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.15)); animation: floatOrganic 3s infinite alternate;">
                    </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown('''
                    <div class="card-joy" style="display: flex; align-items: center; position: relative;">
                        <div style="flex: 1;">
                            <h2 class="result-title">Kondisi Emosional Stabil</h2>
                            <p class="result-desc">Tidak terdeteksi indikasi kelainan mental. Pola bahasa Anda memancarkan keseimbangan emosi dan pikiran yang positif.</p>
                        </div>
                        <img src="https://media.giphy.com/media/l4pTfx2qLszoacZRS/giphy.gif" style="height: 140px; border-radius: 10px; margin-left: 15px; filter: drop-shadow(0 10px 15px rgba(0,0,0,0.15)); animation: floatOrganic 4s infinite alternate;">
                    </div>
                    ''', unsafe_allow_html=True)

                
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown("<p style='color: #5b6e41; font-size: 0.95rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; font-family: Manrope;'>Tingkat Indikasi Emosi</p>", unsafe_allow_html=True)
                st.progress(float(probs[0]), text=f"Kondisi Mental Sehat ({probs[0]:.1%})")
                st.progress(float(probs[1]), text=f"Beban Pikiran & Kecemasan ({probs[1]:.1%})")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Mohon isi teks terlebih dahulu.")
    st.markdown('</div>', unsafe_allow_html=True)

if len(st.session_state['history']) > 0:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="metric-card" style="position: relative; z-index: 1;"><div class="card-header">Consultation log</div>', unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(st.session_state['history']), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
