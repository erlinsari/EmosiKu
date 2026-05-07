import streamlit as st
import streamlit.components.v1 as components
import os
import re
import subprocess
import sys
import socket

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_premium_ui():
    try:
        dist_path = "frontend/dist"
        index_path = os.path.join(dist_path, "index.html")
        assets_path = os.path.join(dist_path, "assets")
        
        if not os.path.exists(index_path):
            return "<h3>Error: File desain tidak ditemukan.</h3>"
        
        with open(index_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        js_files = [f for f in os.listdir(assets_path) if f.endswith(".js")]
        css_files = [f for f in os.listdir(assets_path) if f.endswith(".css")]
        
        if js_files and css_files:
            with open(os.path.join(assets_path, js_files[0]), "r", encoding="utf-8") as f:
                js_code = f.read()
            with open(os.path.join(assets_path, css_files[0]), "r", encoding="utf-8") as f:
                css_code = f.read()
            
            final_html = html_content.replace('</head>', f'<style>{css_code}</style></head>')
            final_html = final_html.replace('</body>', f'<script type="module">{js_code.replace("</script>", "<\\/script>")}</script></body>')
            
            return final_html
        return "<h3>Error: Aset tidak lengkap.</h3>"
    except Exception as e:
        return f"<h3>Kesalahan: {str(e)}</h3>"

# Tampilkan UI
premium_html = get_premium_ui()
if "<h3>" in premium_html:
    st.error(premium_html)
else:
    components.html(premium_html, height=1200, scrolling=True)

# Jalankan Mesin AI secara otomatis
if not is_port_in_use(8000):
    try:
        subprocess.Popen([sys.executable, "api.py"])
        st.toast("🧠 Mesin AI sedang memuat... Mohon tunggu sebentar.")
    except:
        pass
else:
    st.toast("✅ Mesin AI sudah aktif.")
