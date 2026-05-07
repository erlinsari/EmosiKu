import streamlit as st
import torch
import re
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="EmosiKu - Analisis Kesehatan Mental", layout="centered")

# --- LOAD MODEL AI ---
@st.cache_resource
def load_model():
    # Menggunakan model IndoBERT
    model_name = "indobenchmark/indobert-base-p1"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    stopword_remover = StopWordRemoverFactory().create_stop_word_remover()
    return tokenizer, model, stopword_remover

try:
    tokenizer, model, stopword_remover = load_model()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")

# --- FUNGSI PREDIKSI ---
def predict_emotion(text):
    # Pembersihan teks sederhana
    text_clean = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    text_clean = stopword_remover.remove(text_clean)
    
    # Tokenisasi
    inputs = tokenizer(text_clean, return_tensors="pt", truncation=True, max_length=128)
    
    # Prediksi
    with torch.no_grad():
        outputs = model(**inputs)
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        prediction = torch.argmax(probs, dim=-1).item()
        confidence = torch.max(probs).item()
    
    return prediction, confidence

# --- TAMPILAN UTAMA ---
st.title("🧠 EmosiKu")
st.subheader("Analisis Kesehatan Mental Sederhana")
st.write("Bagikan apa yang Anda rasakan, dan AI kami akan memberikan analisis singkat.")

# Input Teks
user_input = st.text_area("Masukkan cerita atau perasaan Anda di sini:", height=150)

if st.button("Analisis Sekarang"):
    if user_input.strip() == "":
        st.warning("Mohon masukkan teks terlebih dahulu.")
    else:
        with st.spinner("Sedang menganalisis..."):
            pred, conf = predict_emotion(user_input)
            
            st.divider()
            
            # Hasil Prediksi
            if pred == 0:
                st.success("### Hasil: Kondisi Stabil")
                st.write("AI kami mendeteksi bahwa pola emosi Anda saat ini dalam keadaan stabil dan sehat.")
            else:
                st.error("### Hasil: Terindikasi Gangguan")
                st.write("AI kami mendeteksi adanya pola emosi yang mungkin mengindikasikan kecemasan atau beban pikiran. Jangan ragu untuk berbagi dengan orang terpercaya.")
            
            # Detail Keyakinan
            st.info(f"Tingkat Keyakinan AI: {conf*100:.2f}%")

st.divider()
st.caption("Aplikasi ini dibuat untuk tujuan edukasi dan screening awal, bukan pengganti diagnosa medis profesional.")
