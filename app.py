import streamlit as st
import streamlit.components.v1 as components
import os
import json
import subprocess
import time

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; background: #ffffff; }
        header, footer { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# --- BAGIAN 1: SERVE TAMPILAN PREMIUM ---
def get_premium_ui():
    base_path = os.getcwd()
    assets_path = os.path.join(base_path, "frontend", "dist", "assets")
    
    if not os.path.exists(assets_path):
        return f"<div style='color:white; padding:20px;'><h3>Error: Folder tidak ditemukan</h3> Path: {assets_path}</div>"
    
    files = os.listdir(assets_path)
    js_file = next((f for f in files if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in files if f.startswith("index-") and f.endswith(".css")), None)
    
    if not js_file or not css_file:
        return f"<div style='color:white; padding:20px;'><h3>Error: File index tidak ditemukan</h3> File di folder: {files}</div>"
    
    try:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        js_json = json.dumps(js_code)
        css_json = json.dumps(css_code)
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <script>
                const cssCode = {css_json};
                const style = document.createElement('style');
                style.textContent = cssCode;
                document.head.appendChild(style);

                window.onload = () => {{
                    const jsCode = {js_json};
                    const blob = new Blob([jsCode], {{type: 'text/javascript'}});
                    const url = URL.createObjectURL(blob);
                    import(url).catch(err => {{
                        document.body.innerHTML = '<h3 style="color:red">JS Error: ' + err + '</h3>';
                    }});
                }};
            </script>
        </head>
        <body><div id="root"></div></body>
        </html>
        """
    except Exception as e:
        return f"<div style='color:white; padding:20px;'><h3>Error Baca File:</h3> {str(e)}</div>"

# Munculkan UI
ui_html = get_premium_ui()
if "Error" in ui_html:
    st.markdown(ui_html, unsafe_allow_html=True)
else:
    components.html(ui_html, height=1200, scrolling=True)

# --- BAGIAN 2: LOGIKA AI ---
if 'api_process' not in st.session_state:
    try:
        st.session_state.api_process = subprocess.Popen(["python", "api.py"])
    except:
        pass
