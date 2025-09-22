# Cybernight Hardware Challenges

## Building / Uploading

Le projet est basé sur [PlatformIO](https://docs.platformio.org/en/latest/integration/ide/vscode.html) avec le framework ESP-IDF.

Pour build et upload :
- ouvrir le dossier racine, contenant `platformio.ini` dans VS Code
- aller dans l'onglet PlatformIO
- sélectionner `Build and Upload` pour la configuration souhaitée

## Ajouter le support d'un devkit

Note : le microcontrolleur doit être compatible (Espressif, assez d'IRAM, support Bluetooth et WiFi)

- Modifier le fichier `platformio.ini`, ajouter la configuration souhaitée en remplaçant la propriété `board` par le microcontrolleur adapté
- entrer dans PlatformIO Core CLI `pio run -t menuconfig -e [nom de la configuration]`
- activer les options suivantes :
    - dans Component config -> Bluetooth
        - activer le bluetooth
        - sélectionner la stack NimBLE
    - dans Compiler options
        - changer l'optimization level pour size

## Pour réussir les challenges

Besoin d'une board Arduino pour prototyper et analyser l'ESP (et à terme le PCB)
