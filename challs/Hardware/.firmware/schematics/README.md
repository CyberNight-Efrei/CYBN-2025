Le EN de l'ATtiny85 est pulldown au lieu d'etre pull up, il faut shortcut le pin RESET' avec VCC pour le faire boot et récupérer le flag en UART (pin 0, 9600 bauds).
