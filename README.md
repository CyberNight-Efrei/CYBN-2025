# Cybernight 2025 - Challlenges

## Créer un challenge :

1. aller dans ``challs/``
2. copier ``0-CHALL-TEMPLATE/``
3. coller dans le dossier de la catégorie
4. renommer le dossier avec le **nom du challenge**
Exemple : ``Web/Challenge 1``

Structure des fichiers d'un challenge :
```shell
challs
╰―<nom de la catégorie>
    ╰―<nom du challenge>
        ╰―src/
            ╰―<fichiers>
        ╰―writeup/
            ╰―README.md
        ╰―.dockerignore     *
        ╰―Dockerfile        *
        ╰―docker-compose.yml*
        ╰―challenge.yml

* = fichiers optionnels

Ne pas renommer les autres dossiers/fichiers !                
```

5. Remplir ``challenge.yml`` avec les informations

L'ensemble des fichiers utiles au challenge, à sa conception, à son docker, et à sa résolution dovient être mis dans ``src/``
Cela peut être un script de solve, des étapes intermédiaires de construction du challenge, ou simplement les fichiers donnés sur le CTFd.

## Synchronier au CTFd

Suivez la [documentation](https://github.com/CTFd/ctfcli)

### Initiaisation

Installer les packages nécessaires
```bash
pip install -r requirements.txt
```

Se connecter à un CTFd
```
ctf init
```

### Ajout de challenges

Ajout un challenge :
```
ctf challenge  add .\challs\<catégorie>\<challenge name>\
```

Tout pousser pour la première fois dans le CTFd :
```
ctf challenge install
```

Pousser un seul challenge pour la première fois dans le CTFd :
```
ctf challenge install <challenge name>
```

### Synchronier les changements

Pour tout synchroniser : 
```
ctf challenge sync
```

Pour synchroniser un seul challenge :
```
ctf challenge sync <challenge name>
```
