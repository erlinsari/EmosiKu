import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="EmosiKu - Debug", layout="wide")

# Gaya dasar
st.markdown("""
    <style>
        .stApp { background: #0f172a; }
        iframe { border: 5px solid red !important; }
    </style>
""", unsafe_allow_html=True)

st.title("EmosiKu Debug Mode")

# Cek keberadaan file
base_path = os.getcwd()
files = os.listdir(base_path)
st.write(f"File di root: {files}")

# Coba render HTML sangat simpel
debug_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { background: red; color: white; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        h1 { font-family: sans-serif; }
    </style>
</head>
<body>
    <h1>IFRAME BEKERJA! (WARNA MERAH)</h1>
</body>
</html>
"""

components.html(debug_html, height=400)

st.write("Jika Anda melihat kotak MERAH di atas, berarti Iframe bekerja.")
