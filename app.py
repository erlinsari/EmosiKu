import streamlit as st
import streamlit.components.v1 as components
import os
import json
import subprocess
import time

# Konfigurasi halaman paling dasar
st.set_page_config(page_title="EmosiKu", layout="wide")

# Tambahkan warna background agar tidak silau
st.markdown("<style>.stApp {background-color: #0f172a;}</style>", unsafe_allow_html=True)

# --- FUNGSI LOADING ASET ---
def render_premium_ui():
    assets_path = "frontend/dist/assets"
    if not os.path.exists(assets_path):
        st.error("Folder assets tidak ditemukan di server.")
        return
    
    files = os.listdir(assets_path)
    js_file = next((f for f in files if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in files if f.startswith("index-") and f.endswith(".css")), None)
    
    if js_file and css_file:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Kirim data ke HTML
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <style>{css_code}</style>
        </head>
        <body>
            <div id="root"></div>
            <script type="module">{js_code}</script>
        </body>
        </html>
        """
        components.html(html_code, height=1200, scrolling=True)
    else:
        st.error("Gagal menemukan file index JS/CSS.")

# Tampilkan UI segera
render_premium_ui()

# --- JALANKAN AI DI BACKGROUND (Tidak Mengganggu UI) ---
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
