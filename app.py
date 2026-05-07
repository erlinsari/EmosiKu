import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# Gunakan background gelap agar transisi mulus
st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; background: #ffffff; }
        header, footer { display: none !important; }
    </style>
""", unsafe_allow_html=True)

def render_premium_ui():
    # URL Mentah dari GitHub (Bertindak sebagai CDN)
    # Ini memastikan file dimuat secara utuh tanpa melewati batasan memori Streamlit
    js_url = "https://raw.githubusercontent.com/erlinsari/EmosiKu/main/frontend/dist/assets/index-BBJjsgNE.js"
    css_url = "https://raw.githubusercontent.com/erlinsari/EmosiKu/main/frontend/dist/assets/index-eQS-I5Sh.css"
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" crossorigin href="{css_url}">
    </head>
    <body>
        <div id="root"></div>
        <script type="module" crossorigin src="{js_url}"></script>
    </body>
    </html>
    """
    components.html(html_code, height=1200, scrolling=True)

# Tampilkan UI segera
render_premium_ui()

# Jalankan AI di latar belakang
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
