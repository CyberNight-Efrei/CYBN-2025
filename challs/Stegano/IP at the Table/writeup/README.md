## Writeup

Chaque numéro de port correspond à un code ASCII décimal qui, une fois converti en caractère, révèle le flag lettre par lettre.

Donc on a :

> 67 89 66 78 123 105 110 115 49 103 104 116 102 117 108 125

Port 67 → ASCII 67 → 'C'  
Port 89 → ASCII 89 → 'Y'  
Port 66 → ASCII 66 → 'B'  
Port 78 → ASCII 78 → 'N'  
etc.

Pour flag ça de manière automatique on peut faire :

```
python3 -c "import re;print(''.join(chr(int(p))for p in re.findall(r'--dport (\d+)',open('chall.rules').read())))"
```
