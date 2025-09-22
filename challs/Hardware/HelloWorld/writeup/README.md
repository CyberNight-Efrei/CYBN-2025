Brancher l'ESP32 sur un port USB, puis
- `ls /dev/ttyUSB*` pour trouver sur quel device est arrivé la sortie de l'ESP
- `picocom -b 115200 /dev/ttyUSB0` pour se connecter en série à l'ESP (`screen` fonctionne également, et `PuTTY` pour Windows)
- Plus qu'à lire le flag sur le terminal :)
