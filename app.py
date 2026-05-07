import streamlit as st
import streamlit.components.v1 as components
import os
import re
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

def get_premium_ui():
    # KITA GUNAKAN FILE YANG ADA DI ROOT (Jalur paling aman saat ini)
    index_path = "index.html"
    assets_path = "assets"
    
    if not os.path.exists(index_path):
        return "<h3>Error: File index.html tidak ditemukan di root.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Deteksi aset di folder root/assets
    js_match = re.search(r'<script .*?src="\./assets/(index-.*?\.js)".*?></script>', html_content)
    css_match = re.search(r'<link .*?href="\./assets/(index-.*?\.css)".*?>', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Injeksi stabil
        new_js = '<script type="module">' + js_code + '</script>'
        new_css = '<style>' + css_code + '</style>'
        
        html_content = html_content.replace(js_match.group(0), new_js)
        html_content = html_content.replace(css_match.group(0), new_css)
        
        return html_content
    
    return f"<h3>Error: Gagal memetakan aset di {assets_path}.</h3>"

# Render
premium_html = get_premium_ui()
components.html(premium_html, height=1200, scrolling=True)

# Jalankan API
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
