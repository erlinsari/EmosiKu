import streamlit as st
import streamlit.components.v1 as components
import os
import json
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; background: #ffffff; }
        header, footer { display: none !important; }
    </style>
""", unsafe_allow_html=True)

def render_premium_ui():
    assets_path = "frontend/dist/assets"
    if not os.path.exists(assets_path):
        st.error("Aset tidak ditemukan. Harap jalankan build.")
        return
    
    files = os.listdir(assets_path)
    js_file = next((f for f in files if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in files if f.startswith("index-") and f.endswith(".css")), None)
    
    if js_file and css_file:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        # Potong JS menjadi beberapa bagian agar tidak terlalu berat saat dikirim
        js_chunks = [js_code[i:i+100000] for i in range(0, len(js_code), 100000)]
        js_chunks_json = json.dumps(js_chunks)
        css_json = json.dumps(css_code)
        
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <style>
                html, body, #root {{ height: 100%; margin: 0; padding: 0; background: #ffffff; }}
                #debug {{ position: fixed; top: 0; left: 0; background: rgba(0,0,0,0.8); color: white; padding: 10px; z-index: 9999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div id="root">
                <div style="display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif; color:#64748b;">
                    🚀 Menyusun Antarmuka EmosiKu...
                </div>
            </div>
            <script>
                (function() {{
                    try {{
                        // Muat CSS
                        const style = document.createElement('style');
                        style.textContent = {css_json};
                        document.head.appendChild(style);

                        // Susun kembali JS dari potongan-potongan
                        const chunks = {js_chunks_json};
                        const fullJs = chunks.join('');
                        
                        const blob = new Blob([fullJs], {{ type: 'text/javascript' }});
                        const url = URL.createObjectURL(blob);
                        
                        const script = document.createElement('script');
                        script.type = 'module';
                        script.src = url;
                        document.head.appendChild(script);
                    }} catch (e) {{
                        document.body.innerHTML = '<h3 style="color:red; padding:20px;">Gagal memuat: ' + e.message + '</h3>';
                    }}
                }})();
            </script>
        </body>
        </html>
        """
        components.html(html_code, height=1200, scrolling=True)

render_premium_ui()

if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
