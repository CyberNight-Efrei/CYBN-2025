## Writeup

Chaque numéro de port correspond à un code ASCII décimal qui, une fois converti en caractère, révèle le flag lettre par lettre.

Donc on a :

> 67 89 66 78 123 65 83 67 49 49 73 115 69 118 51 114 121 119 104 101 114 101 33 125

Port 67 → ASCII 67 → 'C'  
Port 89 → ASCII 89 → 'Y'  
Port 66 → ASCII 66 → 'B'  
Port 78 → ASCII 78 → 'N'  
etc.

Pour flag ça de manière automatique on peut faire :

```
python3 -c "import re;print(''.join(chr(int(p))for p in re.findall(r'--dport (\d+)',open('chall.rules').read())))"
```

=======
## Writeup

Chaque numéro de port correspond à un code ASCII décimal qui, une fois converti en caractère, révèle le flag lettre par lettre.

Donc on a :

> 67 89 66 78 123 65 83 67 49 49 73 115 69 118 51 114 121 119 104 101 114 101 33 125

Port 67 → ASCII 67 → 'C'  
Port 89 → ASCII 89 → 'Y'  
Port 66 → ASCII 66 → 'B'  
Port 78 → ASCII 78 → 'N'  
etc.

Pour flag ça de manière automatique on peut faire :

```
python3 -c "import re;print(''.join(chr(int(p))for p in re.findall(r'--dport (\d+)',open('chall.rules').read())))"
```