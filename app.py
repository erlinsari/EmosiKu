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
        return "<h3>Error: File index.html tidak ditemukan.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Cari nama file JS dan CSS yang aktif
    js_match = re.search(r'src="\./assets/(index-.*?\.js)"', html_content)
    css_match = re.search(r'href="\./assets/(index-.*?\.css)"', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # PENTING: Gunakan .replace() biasa, JANGAN gunakan re.sub() untuk konten JS
        # Karena JS mengandung banyak simbol \ yang bisa bikin error re.sub
        
        tag_js_lama = js_match.group(0) # Ini adalah: src="./assets/index-xxx.js"
        tag_css_lama = css_match.group(0) # Ini adalah: href="./assets/index-xxx.css"
        
        # Kita buat tag baru yang berisi kode aslinya
        # Kita pakai trick: ganti src dengan isi kodenya langsung
        html_content = html_content.replace(f'type="module" crossorigin {tag_js_lama}', '')
        html_content = html_content.replace(f'rel="stylesheet" crossorigin {tag_css_lama}', '')
        
        # Suntikkan kode asli di bagian akhir head dan body
        html_content = html_content.replace('</head>', f'<style>{css_code}</style></head>')
        html_content = html_content.replace('</body>', f'<script type="module">{js_code}</script></body>')
        
        return html_content
    
    return "<h3>Error: Aset gagal dipetakan.</h3>"

# Tampilkan UI
premium_html = get_premium_ui()
components.html(premium_html, height=1200, scrolling=True)

# Jalankan Mesin AI
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen([sys.executable, "api.py"])
        st.session_state.api_started = True
    except:
        pass
