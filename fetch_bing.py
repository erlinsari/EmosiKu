import urllib.request
import re
import os
import base64

def get_bing_image(query):
    print(f"Searching Bing for: {query}")
    url = "https://www.bing.com/images/search?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        # Find the first murl
        match = re.search(r'murl&quot;:&quot;(.*?)&quot;', html)
        if match:
            img_url = match.group(1)
            print(f"Found URL: {img_url}")
            # Download image
            img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            img_data = urllib.request.urlopen(img_req, timeout=10).read()
            # Convert to base64
            b64 = base64.b64encode(img_data).decode('utf-8')
            return f"data:image/png;base64,{b64}"
    except Exception as e:
        print(f"Error: {e}")
    return ""

chars = {
    'sadness': 'inside out sadness transparent png',
    'disgust': 'inside out disgust transparent png',
    'anger': 'inside out anger transparent png',
    'fear': 'inside out fear transparent png',
    'joy': 'inside out joy transparent png',
    'anxiety': 'inside out 2 anxiety transparent png'
}

b64_dict = {}
for name, q in chars.items():
    b64_dict[name] = get_bing_image(q)

with open('images_b64.py', 'w') as f:
    f.write("images = {\n")
    for name, b64 in b64_dict.items():
        f.write(f"    '{name}': '{b64}',\n")
    f.write("}\n")
print("Done writing images_b64.py")
