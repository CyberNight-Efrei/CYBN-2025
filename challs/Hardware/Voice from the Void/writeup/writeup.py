import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from scipy.interpolate import interp1d

try:
    from pydub import AudioSegment
    HAS_PYDUB = True
except ImportError:
    HAS_PYDUB = False

def load_audio(filename):
    """Charge un fichier audio MP3 ou WAV"""
    if filename.lower().endswith('.mp3'):
        if not HAS_PYDUB: raise ImportError("pip install pydub requis pour MP3")
        audio = AudioSegment.from_mp3(filename)
        data = np.array(audio.get_array_of_samples()).astype(float)
        if audio.channels == 2: data = data.reshape((-1, 2))[:, 0]
        return audio.frame_rate, data
    else:
        sr, data = wavfile.read(filename)
        if len(data.shape) > 1: data = data[:, 0]
        return sr, data.astype(float)

def demodulate_am(audio, sr, carrier_freq=2400):
    """Démodule un signal AM"""
    t = np.arange(len(audio)) / sr
    
    # Démodulation I/Q
    i = audio * np.cos(2 * np.pi * carrier_freq * t)
    q = audio * np.sin(2 * np.pi * carrier_freq * t)
    
    # Filtre passe-bas (cutoff = 2 lignes/sec * 2080 pixels)
    cutoff = 4160 / (sr / 2)
    b, a = signal.butter(5, cutoff, btype='low')
    
    i_filt = signal.filtfilt(b, a, i)
    q_filt = signal.filtfilt(b, a, q)
    
    return np.sqrt(i_filt**2 + q_filt**2)

def reconstruct_image(envelope, sr, line_rate=2, width=2080):
    """Reconstruit l'image depuis l'enveloppe"""
    samples_per_line = sr // line_rate
    num_lines = len(envelope) // samples_per_line
    
    # Reshape en matrice
    img = envelope[:num_lines * samples_per_line].reshape(num_lines, samples_per_line)
    
    # Rééchantillonner à 2080 pixels par ligne
    img_resampled = np.zeros((num_lines, width))
    for i in range(num_lines):
        f = interp1d(np.linspace(0, 1, samples_per_line), img[i], kind='linear')
        img_resampled[i] = f(np.linspace(0, 1, width))
    
    # Normaliser 0-255
    img_norm = (img_resampled - img_resampled.min()) / (img_resampled.max() - img_resampled.min())
    return (img_norm * 255).astype(np.uint8)

def solve_apt(filename):
    """Solver complet pour le challenge APT"""
    print(f"[+] Chargement: {filename}")
    sr, audio = load_audio(filename)
    audio = audio / max(abs(audio.max()), abs(audio.min()))
    
    print(f"[+] Sample rate: {sr} Hz, Durée: {len(audio)/sr:.1f}s")
    print("[+] Démodulation AM à 2400 Hz...")
    
    envelope = demodulate_am(audio, sr, carrier_freq=2400)
    
    print("[+] Reconstruction image (2080x? pixels, 2 lignes/sec)...")
    image = reconstruct_image(envelope, sr, line_rate=2, width=2080)
    
    print(f"[+] Image finale: {image.shape[0]}x{image.shape[1]} pixels")
    
    plt.figure(figsize=(15, 8))
    plt.imshow(image, cmap='gray', aspect='auto')
    plt.title('Voice from the Void')
    plt.colorbar(label='Intensité')
    plt.tight_layout()
    plt.savefig('decoded.png', dpi=150)
    plt.show()
    
    print("[+] Image sauvegardée: decoded.png")
    return image

if __name__ == "__main__":
    image = solve_apt('voice.wav')
    print("\nFlag visible dans l'image")