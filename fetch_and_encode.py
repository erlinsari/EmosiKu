import os
import base64
import requests
from duckduckgo_search import DDGS

chars = ['Joy', 'Sadness', 'Anxiety', 'Anger', 'Disgust', 'Fear']
base64_strings = {}

def get_image(character):
    print(f"Searching for {character}...")
    results = DDGS().images(f"{character} inside out png transparent", max_results=5)
    for res in results:
        url = res['image']
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                print(f"Success downloaded {character}")
                return base64.b64encode(r.content).decode('utf-8')
        except:
            continue
    return ""

for c in chars:
    base64_strings[c.lower()] = get_image(c)

with open('images_b64.py', 'w') as f:
    f.write("images = {\n")
    for k, v in base64_strings.items():
        if v:
            f.write(f"    '{k}': 'data:image/png;base64,{v}',\n")
    f.write("}\n")
print("Done writing images_b64.py")
