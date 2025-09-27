from PIL import Image
import numpy as np

def read_lsb_last_lines(image_path, num_lines=20):
    """Lit les LSB des 20 dernières lignes d'une image"""
    
    # Ouvrir l'image
    img = Image.open(image_path)
    pixels = np.array(img)
    height, width, channels = pixels.shape
    
    print(f"Image: {width}x{height}, Channels: {channels}")
    print(f"Lecture des {num_lines} dernières lignes...\n")
    
    # Lire chaque ligne
    for line_offset in range(num_lines):
        line_idx = height - num_lines + line_offset
        binary_data = ""
        
        # Extraire les LSB de tous les pixels de la ligne
        for x in range(width):
            for c in range(channels):
                binary_data += str(pixels[line_idx, x, c] & 1)
        
        # Convertir binaire en texte
        text = ""
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            if len(byte) == 8:
                char_code = int(byte, 2)
                # Afficher seulement les caractères imprimables
                if 32 <= char_code <= 126: text += chr(char_code)
                else: text += '.'
        
        print(f"Ligne {line_idx + 1}: {text[:100]}")  # Afficher les 100 premiers caractères
    
    print("\n✓ Lecture terminée")


if __name__ == "__main__":
    image_path = "Cicada 3302.png"
    read_lsb_last_lines(image_path, num_lines=20)