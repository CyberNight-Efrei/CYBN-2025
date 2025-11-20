Les valeurs entre parenthèses suivent clairement la suite de Fibonacci : 0, 1, 1, 2, 3, 5, 8, 13, 21...  
Les mots de passe sont des hashs hexadécimaux de 16 caractères. On teste différents formats avec SHA256 :

```py
import hashlib

# Test simple
hashlib.sha256("0".encode()).hexdigest()[:16]
# 5feceb66ffc86f38 - Match pour Layer 0

hashlib.sha256("1".encode()).hexdigest()[:16]
# 6b86b273ff34fce1 - Match pour Layer 1 et 2

hashlib.sha256("2".encode()).hexdigest()[:16]
# d4735e3a265e16ee - Match pour Layer 3
```

Le pattern est simple : chaque mot de passe est le SHA256 du nombre de Fibonacci correspondant, tronqué à 16 caractères.  
Format : `sha256(str(fibonacci(layer)))[:16]`  
Flag : `CYBN{M4tryoshk4sAga1nAndAg4in}`
