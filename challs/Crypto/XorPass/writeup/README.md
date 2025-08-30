Une simple backup XML de KeePass, très certainement XORed : possible de faire une comparaison par clair connu :

- créer backup d'une database keepass en XML
- prendre la première ligne, s'en servir comme clé XOR avec la backup chiffrée
- récupérer une taille conséquentee pour la clé hexa (~50 caractères)
- retirer des caractères 1 par 1 à la fin de la clé jusqu'à ce que ça déchiffre la vraie backup
- profit : `CYBN{X0R_yOU_ShoULd_N0T_YouR_B1Ckup5}`



Passphrase : `JeSuisLaCybernight9LaVraie` -> (PBKDF2 SHA256) Password : `1f461f9e6490378deaed5a7216cad56829a8e16a0489dd6b5f6be29682e2a165`

Flag : `CYBN{X0R_yOU_ShoULd_N0T_YouR_B1Ckup5}`

Passphrase : `JeSuisLaCybernight9LaVraie` -> (PBKDF2 SHA1) XOR KEY : `cb09f516b0e92e35c6a630b9d9ba1239`