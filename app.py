import streamlit as st
import streamlit.components.v1 as components
import os
import re
import subprocess
import sys

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

def get_premium_ui():
    index_path = "index.html"
    assets_path = "assets"
    
    if not os.path.exists(index_path):
        return "<h3>Error: File index.html tidak ditemukan di root.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Deteksi aset menggunakan regex yang lebih fleksibel
    js_match = re.search(r'src="\./assets/(index-.*?\.js)"', html_content)
    css_match = re.search(r'href="\./assets/(index-.*?\.css)"', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Pembersihan karakter rawan
        safe_js = js_code.replace('</script>', '<\\/script>')
        
        # Injeksi Desain Premium
        new_js = f'<script type="module">{safe_js}</script>'
        new_css = f'<style>{css_code}</style>'
        
        # Ganti tag lama dengan kode asli (Inline)
        html_content = re.sub(r'<script type="module" crossorigin src="\./assets/index-.*?\.js"></script>', new_js, html_content)
        html_content = re.sub(r'<link rel="stylesheet" crossorigin href="\./assets/index-.*?\.css">', new_css, html_content)
        
        return html_content
    
    return f"<h3>Error: Aset gagal dimuat. Pastikan folder '{assets_path}' lengkap.</h3>"

# Render UI Premium
premium_html = get_premium_ui()
components.html(premium_html, height=1200, scrolling=True)

# Jalankan Mesin AI (api.py)
if 'api_started' not in st.session_state:
    try:
        # Gunakan sys.executable agar kompatibel dengan Linux/Windows di cloud
        subprocess.Popen([sys.executable, "api.py"])
        st.session_state.api_started = True
    except Exception as e:
        st.write(f"⚠️ Status AI: Sedang inisialisasi... ({e})")
