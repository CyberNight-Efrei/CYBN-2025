## Writeup

Dans ce chall j'ai joué sur les micro variations du canal R d'une image pour simuler le principe de changement de température de la stéganographie thermique. Vous pouvez voir ça comme une variante du LSB qui mêle analyse différentielle et manipulation du canal rouge :D

## Le concept

Image 1 : Image de référence (originale)
Image 2 : Image modifiée contenant le message caché
Comme je l'ai dit au dessus, les deux images semblent identiques à l'œil nu, mais contiennent des micro variations dans le canal rouge.

## Mécanisme d'encodage

Le message est caché bit par bit dans les pixels :

Bit '0' → Le canal rouge de l'image modifiée est diminué par rapport à la référence
Bit '1' → Le canal rouge de l'image modifiée est augmenté par rapport à la référence

Les variations sont minimes (±1 ou ±2 sur une échelle de 0-255), invisibles pour l'œil humain mais détectables par analyse. zsteg ne marche pas pour résoudre le chall, puisqu'il cherche des patterns LSB classiques dans une image, alors que cette technique nécessite la comparaison de deux PNG.

> Script de résolution joint à cette writeup.
