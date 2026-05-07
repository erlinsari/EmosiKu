import streamlit as st
import streamlit.components.v1 as components
import os
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# Background agar tidak silau
st.markdown("<style>.stApp {background-color: #0f172a;}</style>", unsafe_allow_html=True)

def main():
    # KITA GUNAKAN SISTEM LANGSUNG TANPA BACA FILE
    # Saya akan mencoba memuat versi CDN yang paling stabil sekali lagi dengan sistem yang lebih bersih
    
    js_url = "https://cdn.jsdelivr.net/gh/erlinsari/EmosiKu/assets/index-BBJjsgNE.js"
    css_url = "https://cdn.jsdelivr.net/gh/erlinsari/EmosiKu/assets/index-eQS-I5Sh.css"
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" crossorigin href="{css_url}">
        <style>
            html, body, #root {{ height: 100%; margin: 0; padding: 0; background: #ffffff; }}
        </style>
    </head>
    <body>
        <div id="root"></div>
        <script type="module" crossorigin src="{js_url}"></script>
    </body>
    </html>
    """
    
    components.html(html_content, height=1200, scrolling=True)

main()

# Jalankan API
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
