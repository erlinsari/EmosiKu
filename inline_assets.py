import os

# Ambil dari folder build asli
dist = os.path.join('frontend', 'dist')
assets = os.path.join(dist, 'assets')
output_dir = 'web'
output_html = os.path.join(output_dir, 'index.html')

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Cari file terbaru
js_files = [f for f in os.listdir(assets) if f.endswith('.js')]
css_files = [f for f in os.listdir(assets) if f.endswith('.css')]

if not js_files or not css_files:
    print("Error: File build tidak ditemukan!")
    exit(1)

js_file = js_files[0]
css_file = css_files[0]

print(f"Menggabungkan {js_file} dan {css_file}...")

with open(os.path.join(assets, js_file), 'r', encoding='utf-8') as f:
    js_code = f.read()
with open(os.path.join(assets, css_file), 'r', encoding='utf-8') as f:
    css_code = f.read()

# Buat HTML baru yang bersih
new_html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EmosiKu Premium</title>
    <style>
    {css_code}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="module">
    {js_code}
    </script>
</body>
</html>"""

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Berhasil menggabungkan ke {output_html}!")
