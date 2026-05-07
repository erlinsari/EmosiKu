import streamlit as st
import streamlit.components.v1 as components
import os
import json
import subprocess
import time

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# Tampilkan Style CSS Dasar Streamlit segera
st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; background: #ffffff; }
        header, footer { display: none !important; }
        .stMain { padding: 0 !important; }
    </style>
""", unsafe_allow_html=True)

# --- BAGIAN 1: SERVE TAMPILAN PREMIUM (Dijalankan Segera) ---
def get_premium_ui():
    assets_path = "frontend/dist/assets"
    if not os.path.exists(assets_path):
        return "<h3>Error: Folder assets tidak ditemukan.</h3>"
    
    js_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".css")), None)
    
    if js_file and css_file:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()
            
        js_json = json.dumps(js_code)
        css_json = json.dumps(css_code)
        
        # Template HTML yang dioptimasi
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <style>html,body,#root{{height:100%;margin:0;padding:0;}}</style>
            <script>
                const cssCode = {css_json};
                const style = document.createElement('style');
                style.textContent = cssCode;
                document.head.appendChild(style);

                window.onload = () => {{
                    const jsCode = {js_json};
                    const blob = new Blob([jsCode], {{type: 'text/javascript'}});
                    const url = URL.createObjectURL(blob);
                    import(url).catch(console.error);
                }};
            </script>
        </head>
        <body><div id="root"></div></body>
        </html>
        """
    return "<h3>Error: Aset tidak ditemukan.</h3>"

# Munculkan UI Premium
ui_html = get_premium_ui()
components.html(ui_html, height=1200, scrolling=True)

# --- BAGIAN 2: LOGIKA AI (Dimuat di Latar Belakang) ---
# Kita gunakan placeholder agar user tahu proses AI sedang berjalan di belakang layar
status_placeholder = st.empty()

if 'api_process' not in st.session_state:
    with status_placeholder:
        st.info("🔄 Mengaktifkan Mesin AI EmosiKu... Mohon tunggu sebentar.")
    
    # Jalankan API
    try:
        st.session_state.api_process = subprocess.Popen(["python", "api.py"])
        time.sleep(5) # Beri waktu API untuk loading model
        status_placeholder.empty()
        st.success("✅ AI EmosiKu Siap!")
        time.sleep(2)
        st.rerun() # Refresh sekali agar sukses menghilang dan fokus ke UI
    except Exception as e:
        st.error(f"Gagal menjalankan AI: {e}")
