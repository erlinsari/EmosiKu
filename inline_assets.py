import os

dist = 'web'
assets = os.path.join(dist, 'assets')
html_path = os.path.join(dist, 'index.html')

# Cari file terbaru
js_file = [f for f in os.listdir(assets) if f.endswith('.js')][0]
css_file = [f for f in os.listdir(assets) if f.endswith('.css')][0]

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

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Berhasil menggabungkan ke web/index.html!")
