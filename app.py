import streamlit as st
import streamlit.components.v1 as components
import os
import re
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

def get_premium_ui():
    index_path = "index.html"
    assets_path = "assets"
    
    if not os.path.exists(index_path):
        return "<h3>Error: File index.html tidak ditemukan.</h3>"
    
    with open(index_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    js_match = re.search(r'<script .*?src="\./assets/(index-.*?\.js)".*?></script>', html_content)
    css_match = re.search(r'<link .*?href="\./assets/(index-.*?\.css)".*?>', html_content)
    
    if js_match and css_match:
        js_file = js_match.group(1)
        css_file = css_match.group(1)
        
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # PENTING: Escape karakter yang bisa merusak tag HTML
        # Kita gunakan metode pembersihan yang lebih aman
        safe_js = js_code.replace('</script>', '<\\/script>')
        
        new_js = f'<script type="module">{safe_js}</script>'
        new_css = f'<style>{css_code}</style>'
        
        # Ganti tag asli dengan kode yang sudah dibersihkan
        html_content = html_content.replace(js_match.group(0), new_js)
        html_content = html_content.replace(css_match.group(0), new_css)
        
        return html_content
    
    return "<h3>Error: Gagal memetakan aset desain.</h3>"

# Tampilkan UI
premium_html = get_premium_ui()
components.html(premium_html, height=1200, scrolling=True)

# Jalankan API di latar belakang
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
