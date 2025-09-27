import base64

# Copier le contenu du Gbin
with open('file.txt', 'r') as f: b64_data = f.read()
png_data = base64.b64decode(b64_data) # Décoder
with open('recovered.png', 'wb') as f: f.write(png_data) # Recréer le PNG