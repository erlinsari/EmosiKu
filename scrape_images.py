import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_image_url(character):
    url = f"https://disney.fandom.com/wiki/{character}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Look for the main infobox image
            img = soup.select_one('aside.portable-infobox figure.pi-image img.pi-image-thumbnail')
            if img and img.has_attr('src'):
                # Extract URL before the /revision/latest part
                src = img['src']
                if '/revision/latest' in src:
                    src = src.split('/revision/latest')[0]
                return src
    except Exception as e:
        print(e)
    return None

chars = ['Sadness', 'Joy', 'Anger', 'Fear', 'Disgust', 'Anxiety_(Inside_Out)']
urls = {}
for c in chars:
    urls[c] = get_image_url(c)

print(urls)
