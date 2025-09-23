En lisant le code source donné avec l'énoncé, on se rend compte assez rapidement qu'il va falloir lire le flag en série, cependant n'est donné ni le baud rate, ni les options de bits. Essayer les deux baud rates les plus classique ne donne rien, et on est limité par la librairie `SoftwareSerial` qui ne supporte pas les options pour la communication série. On se retrouve donc face à un probleème : l'Arduino Nano ne possède qu'un port série hardware, qui sera utilisé pour la communication avec l'ESP, et on ne connait pas les réglages de la communication. 

Le code source nous indique que les données envoyées par l'ESP contiennent la chaîne de caractères `CYBN{`, on en déduit qu'on doit bruteforce les paramètres en cherchant cette chaîne. On peut donc supprimer toutes les options envoyant moins de 7 bits (ici les lettres sont en ASCII latin, qui s'écrit avec 7 bits).

Comme on ne peut pas communiquer en temps réel l'avancement du bruteforce, la stratégie sera la suivante :
1. Bruteforce sans log, le port série communique avec l'ESP. On peut s'assurer du bon fonctionnement du bruteforce par le clignotement de la LED "RX".
2. Indiquer un succès ou une erreur en faisant clignoter à deux fréquences différentes la LED builtin (accessible avec la macro `LED_BUILTIN`).
3. Écrire, si c'est un succès, les paramètres dans l'EEPROM (mémoire non-volatile dans l'Arduino).
4. Re-flasher l'Arduino, et récuperer ces valeurs à l'aide d'un autre programme et de la liaison série avec le PC.

Le programme permettant de faire cela est disponible ici : `src/writeup/writeup.ino`
