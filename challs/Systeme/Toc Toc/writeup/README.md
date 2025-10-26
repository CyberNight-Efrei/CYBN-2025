Toc Toc et une liste de ports font référence à un concept : le **Port Knocking**

Le concept est le suivant : le port cible est fermé, mais s'ouvre quand on envoi une requete dans l'odre à une suite de ports bien définis.
Ref : [https://fr.wikipedia.org/wiki/Port_knocking](https://fr.wikipedia.org/wiki/Port_knocking)

Ici on a alors trois ports, ainsi qu'un configuration SSH dite "par défaut", autrement dit il écoute sur le port 22

Il faut donc lancer une requete TCP dans l'ordre vers chacun des trois ports, puis ensuite ouvrir la connexion SSH au port 22

On peut le faire manuellement à l'aide de `telnet` ou `nc`, sinon en utilisant le client `knockd` :
1.
```bash
telnet 10.44.10.144 7854 
telnet 10.44.10.144 1803 
telnet 10.44.10.144 4576

ssh neuill@10.44.10.144
```

```bash
nc 10.44.10.144 7854 
nc 10.44.10.144 1803 
nc 10.44.10.144 4576

ssh neuill@10.44.10.144
```

2.

```bash
apt install knockd
knock 10.44.10.144 -v 7854 1803 4576 
```

Une fois connecté : 
```bash
ls
cat flag.txt
CYBN{T0c_t0c_h3R35_ThE_P0rT_Kn0Ck1nG}
```