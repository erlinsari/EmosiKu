import streamlit as st
import os
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# Background Dasar
st.markdown("<style>.stApp {background-color: #0f172a;}</style>", unsafe_allow_html=True)

def render_ui():
    assets_path = "assets"
    
    # Cari file
    js_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".js")), None)
    css_file = next((f for f in os.listdir(assets_path) if f.startswith("index-") and f.endswith(".css")), None)
    
    if js_file and css_file:
        with open(os.path.join(assets_path, js_file), "r", encoding="utf-8") as f:
            js_code = f.read()
        with open(os.path.join(assets_path, css_file), "r", encoding="utf-8") as f:
            css_code = f.read()

        # Kita gunakan manual Iframe dengan srcdoc
        # Kita bungkus CSS dan JS secara murni tanpa link luar sama sekali
        html_code = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <style>{css_code}</style>
        </head>
        <body>
            <div id="root"></div>
            <script type="module">{js_code}</script>
        </body>
        </html>
        """
        
        # Gunakan st.write dengan unsafe_allow_html untuk memaksa Iframe muncul
        # Ini adalah cara paling "kasar" tapi paling ampuh jika sistem komponen diblokir
        st.write(
            f'<iframe srcdoc="{html_code.replace('"', '&quot;')}" width="100%" height="1500" style="border:none; background:white;"></iframe>',
            unsafe_allow_html=True
        )
    else:
        st.error("Aset desain tidak ditemukan. Harap hubungi admin.")

render_ui()

# Jalankan API
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
