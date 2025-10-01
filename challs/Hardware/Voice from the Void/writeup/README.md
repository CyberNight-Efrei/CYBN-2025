## Writeup :

**Étape 1 : Démodulation AM**
Pour extraire l'image, nous devons démoduler le signal AM à 2400 Hz. La méthode classique est la détection synchrone (démodulation I/Q) :

```py
t = np.arange(len(audio)) / sample_rate
**Multiplier par cos et sin de la porteuse**
i_signal = audio * np.cos(2 * np.pi * 2400 * t)
q_signal = audio * np.sin(2 * np.pi * 2400 * t)
```

**Étape 2 : Filtrage passe-bas**
Après multiplication, on obtient des composantes haute fréquence qu'il faut éliminer :

```py
# Fréquence de coupure = 2 lignes/sec × 2080 pixels = 4160 Hz
cutoff = 4160 / (sample_rate / 2)
b, a = signal.butter(5, cutoff, btype='low')

i_filtered = signal.filtfilt(b, a, i_signal)
q_filtered = signal.filtfilt(b, a, q_signal)
```

**Étape 3 : Calcul de l'enveloppe**
L'enveloppe du signal AM est la magnitude du signal I/Q :

```py
envelope = np.sqrt(i_filtered**2 + q_filtered**2)
```

**Étape 4 : Reconstruction de l'image**
Le signal contient les lignes de l'image de manière séquentielle :

```py
samples_per_line = sample_rate // 2  # 2 lignes/seconde
num_lines = len(envelope) // samples_per_line
# Reshape en matrice
image = envelope[:num_lines * samples_per_line].reshape(num_lines, samples_per_line)
```

**Étape 5 : Rééchantillonnage**
Chaque ligne doit être rééchantillonnée à 2080 pixels :

```py
for i in range(num_lines):
    f = interp1d(np.linspace(0, 1, samples_per_line), image[i], kind='linear')
    image_resampled[i] = f(np.linspace(0, 1, 2080))
```
