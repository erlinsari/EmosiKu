import streamlit as st
import streamlit.components.v1 as components
import os
import re
import subprocess
import sys

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

def get_premium_ui():
    try:
        index_path = "index.html"
        assets_path = "assets"
        
        if not os.path.exists(index_path):
            return "<h3>Error: File index.html tidak ditemukan.</h3>"
        
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Cari file JS dan CSS apapun yang ada di folder assets
        # Ini jauh lebih aman daripada mencari lewat regex di index.html
        js_files = [f for f in os.listdir(assets_path) if f.endswith(".js") and f.startswith("index-")]
        css_files = [f for f in os.listdir(assets_path) if f.endswith(".css") and f.startswith("index-")]
        
        if js_files and css_files:
            # Ambil file yang paling baru (paling atas)
            js_file = js_files[0]
            css_file = css_files[0]
            
            with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
                js_code = f.read()
            with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
                css_code = f.read()
            
            # Bersihkan index.html dari pemanggilan file eksternal agar tidak bentrok
            html_content = re.sub(r'<script type="module" crossorigin src="\./assets/index-.*?\.js"></script>', '', html_content)
            html_content = re.sub(r'<link rel="stylesheet" crossorigin href="\./assets/index-.*?\.css">', '', html_content)
            
            # Suntikkan kode asli secara langsung (Metode paling stabil)
            final_html = html_content.replace('</head>', f'<style>{css_code}</style></head>')
            final_html = final_html.replace('</body>', f'<script type="module">{js_code.replace("</script>", "<\\/script>")}</script></body>')
            
            return final_html
        
        return f"<h3>Error: Aset tidak ditemukan di folder '{assets_path}'.</h3>"
    except Exception as e:
        return f"<h3>Terjadi kesalahan sistem: {str(e)}</h3>"

# Render
premium_html = get_premium_ui()
if "<h3>" in premium_html:
    st.error(premium_html)
else:
    components.html(premium_html, height=1200, scrolling=True)

# Jalankan Mesin AI
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen([sys.executable, "api.py"])
        st.session_state.api_started = True
    except:
        pass
