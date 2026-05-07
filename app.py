import streamlit as st
import streamlit.components.v1 as components
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")

# Background agar tidak silau
st.markdown("""
    <style>
        .stApp { background: #0f172a; margin: 0; padding: 0; }
        iframe { border: none !important; width: 100%; min-height: 100vh; background: #ffffff; }
        header, footer { display: none !important; }
    </style>
""", unsafe_allow_html=True)

def render_premium_ui():
    # Menggunakan jsDelivr (Layanan CDN Resmi untuk GitHub)
    # Ini menjamin file terbaca sebagai JavaScript yang valid oleh browser
    js_url = "https://cdn.jsdelivr.net/gh/erlinsari/EmosiKu/frontend/dist/assets/index-BBJjsgNE.js"
    css_url = "https://cdn.jsdelivr.net/gh/erlinsari/EmosiKu/frontend/dist/assets/index-eQS-I5Sh.css"
    
    html_code = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" crossorigin href="{css_url}">
        <style>
            html, body, #root {{ height: 100%; margin: 0; padding: 0; }}
            .loading-text {{ 
                display: flex; justify-content: center; align-items: center; 
                height: 100vh; font-family: sans-serif; color: #64748b;
            }}
        </style>
    </head>
    <body>
        <div id="root">
            <div class="loading-text">Memuat Antarmuka EmosiKu...</div>
        </div>
        <script type="module" crossorigin src="{js_url}"></script>
    </body>
    </html>
    """
    components.html(html_code, height=1200, scrolling=True)

# Eksekusi UI
render_premium_ui()

# Aktifkan AI
if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
