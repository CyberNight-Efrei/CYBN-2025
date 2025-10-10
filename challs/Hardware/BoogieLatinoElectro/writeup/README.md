On comprend par la description qu'on à affaire à une technologie sans fil, sûrement du Bluetooth.

En utilisant nRF Tools sur un téléphone, on trouve effectivement un appareil Bluetooth avec le bon nom (donné en connexion série au challenge "Hello, World!"). On peut ainsi initialiser la connection avec l'ESP32, qui propose un serveur BLE GATT.

On énumère les propriétés disponibles, il n'y en a qu'une seule disponible uniquement à la lecture. En la demandant, on obtient le flag.
