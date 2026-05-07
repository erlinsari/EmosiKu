import streamlit as st
import streamlit.components.v1 as components
import subprocess

st.set_page_config(page_title="EmosiKu - AI Psychotherapy", layout="wide")
st.markdown("<style>.stApp {background-color: #0f172a;}</style>", unsafe_allow_html=True)

def main():
    # URL ASET (jsDelivr dengan versi terbaru agar tidak cache)
    # Kita tambahkan timestamp agar browser selalu mengambil yang paling baru
    js_url = "https://cdn.jsdelivr.net/gh/erlinsari/EmosiKu/assets/index-BBJjsgNE.js"
    css_url = "https://cdn.jsdelivr.net/gh/erlinsari/EmosiKu/assets/index-eQS-I5Sh.css"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8" />
        <link rel="stylesheet" crossorigin href="{css_url}">
        <style>
            html, body, #root {{ height: 100%; margin: 0; padding: 0; background: #ffffff; }}
            #error-log {{ 
                position: fixed; bottom: 0; left: 0; width: 100%; 
                background: #fee2e2; color: #991b1b; padding: 10px; 
                font-family: monospace; font-size: 12px; z-index: 9999;
                display: none; border-top: 2px solid #ef4444;
            }}
        </style>
    </head>
    <body>
        <div id="root">
            <div style="padding: 50px; text-align: center; color: #64748b; font-family: sans-serif;">
                <h2>🚀 Menyambungkan ke Desain EmosiKu...</h2>
                <p>Jika layar tetap seperti ini lebih dari 10 detik, berarti ada kendala koneksi.</p>
            </div>
        </div>
        <div id="error-log"></div>

        <script>
            // SISTEM PELACAK ERROR
            const log = document.getElementById('error-log');
            window.onerror = function(msg, url, line) {{
                log.style.display = 'block';
                log.innerHTML += '❌ ERROR: ' + msg + ' (Line: ' + line + ')<br>';
            }};

            console.error = (function(old) {{
                return function(msg) {{
                    log.style.display = 'block';
                    log.innerHTML += '⚠️ CONSOLE: ' + msg + '<br>';
                    old.apply(console, arguments);
                }};
            }})(console.error);
        </script>
        
        <script type="module" crossorigin src="{js_url}"></script>
    </body>
    </html>
    """
    
    components.html(html_content, height=1200, scrolling=True)

main()

if 'api_started' not in st.session_state:
    try:
        subprocess.Popen(["python", "api.py"])
        st.session_state.api_started = True
    except:
        pass
