## Writeup

L'image fournie n'a rien de visible à l'oeil nu, mais on remarque que son ratio est légèrement au dessus du 16:9 (1920x1080) habituel, puisqu'elle fait du 1920x1100. On peut donc se douter que quelque chose se cache dans les 20 dernières lignes. Même sans ce raisonnement, une recherche concernant les LSB révèle que quelque chose se cache en bas de l'image.

Avec un script adapté (`read_lsb_20_last_lines.py`), on trouve un lien gbin.me : `gbin.me/fWZEDdpW7cb0HpNh`

Ce lien redirige vers un bloc de base64 qui, correctement décodé, révèle un QR Code (`base64_to_png.py`), dont le format PNG est reconnaissable à la signature. Attention à ne pas décoder et coller le résultat dans un fichier texte que vous changeriez en PNG à la main : le bloc-note corrompt les fichiers binaires.
Mais ici, petit piège : décoder le QR Code ne sert à rien puisqu'on obtient :

```
You have clearly missed a crucial piece of information.
Pay attention.

3302
```

On se doute alors que quelque chose est caché autre part. Cette fois, rien ne se cache dans les LSB, mais dans les métadonnées, rapidement vérifiables avec exiftool. Le champ de la description révèle un code morse : `−·−· −·−− −··· −· {·−− ···−− ·−·· −·−· −−−−− −− · ·− −− −−− −· −−· ··− ··· ··· ··· −·−·−− −·−·−− }`

Bingo, vous avez le flag : `CYBN{W3LC0MEAMONGUSSS!!}`
