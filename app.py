import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# Tampilkan status di Streamlit agar kita tahu apa yang terjadi
status = st.empty()
status.info("⏳ Sedang menyiapkan antarmuka premium...")

def render_ui():
    try:
        # Gunakan file yang ada di root
        index_path = "index.html"
        assets_path = "assets"
        
        if not os.path.exists(index_path):
            st.error("File index.html tidak ditemukan di root.")
            return

        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
        # Cari file JS dan CSS asli
        js_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".js")), None)
        css_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".css")), None)
        
        if js_file and css_file:
            with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
                js_code = f.read()
            with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
                css_code = f.read()
            
            # Suntikkan CSS ke dalam tag <style>
            html_content = html_content.replace("</head>", f"<style>{css_code}</style></head>")
            
            # Suntikkan JS ke dalam tag <script>
            # Kita hapus pemanggilan file lama dan ganti dengan kode asli
            html_content = html_content.replace('<script type="module" crossorigin src="./assets/', '<!--')
            html_content = html_content.replace('.js"></script>', '-->')
            html_content += f'<script type="module">{js_code}</script>'
            
            components.html(html_content, height=1200, scrolling=True)
            status.empty() # Hapus status jika berhasil
        else:
            st.error("File aset JS/CSS tidak ditemukan di folder assets.")
            
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat tampilan: {e}")

# Jalankan perenderan
render_ui()

# Jalankan API AI
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
