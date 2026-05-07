import os
import requests

def download_image(url, filename):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://en.wikipedia.org/'
    }
    print(f"Downloading {filename}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Success: {filename}")
        else:
            print(f"Failed to download {filename}: Status {response.status_code}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

os.makedirs('images', exist_ok=True)

# List of Wikipedia Image URLs
images = {
    'images/sadness.png': 'https://upload.wikimedia.org/wikipedia/en/6/66/Sadness_%28Inside_Out%29.png',
    'images/disgust.png': 'https://upload.wikimedia.org/wikipedia/en/b/b5/Disgust_%28Inside_Out%29.png',
    'images/anger.png': 'https://upload.wikimedia.org/wikipedia/en/9/91/Anger_%28Inside_Out%29.png',
    'images/fear.png': 'https://upload.wikimedia.org/wikipedia/en/0/04/Fear_%28Inside_Out%29.png',
    'images/joy.png': 'https://upload.wikimedia.org/wikipedia/en/c/c7/Joy_%28Inside_Out%29.png',
    'images/anxiety.png': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/Anxiety_%28Inside_Out_2%29.png/220px-Anxiety_%28Inside_Out_2%29.png'
}

for filename, url in images.items():
    download_image(url, filename)
