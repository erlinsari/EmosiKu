import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

st.set_page_config(page_title="EmosiKu", layout="wide")
st.markdown("<style>.stApp {background-color: #0f172a;}</style>", unsafe_allow_html=True)

def render_premium_ui():
    assets_path = "frontend/dist/assets"
    if not os.path.exists(assets_path):
        st.error(f"Folder assets tidak ditemukan. Path: {os.path.abspath(assets_path)}")
        return
    
    files = os.listdir(assets_path)
    js_file = next((f for f in files if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in files if f.startswith("index-") and f.endswith(".css")), None)
    
    if js_file and css_file:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # GABUNGKAN SECARA MANUAL (Sangat Aman)
        html_start = """<!DOCTYPE html><html><head><meta charset="UTF-8" /><style>"""
        html_middle = """</style></head><body><div id="root"></div><script type="module">"""
        html_end = """</script></body></html>"""
        
        full_html = html_start + css_code + html_middle + js_code + html_end
        components.html(full_html, height=1200, scrolling=True)
    else:
        st.error(f"Gagal menemukan aset. File tersedia: {files}")

render_premium_ui()

if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
