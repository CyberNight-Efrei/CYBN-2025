- ouvrir ls .csv avec un editeur de texte ou un lecteur de tableau
- trouver les lignes avec comme "Rule title" : "Dumping of Sensitive Hives Via Reg.EXE"
- dans la colonne "Details" de ces lignes, on trouve les trois noms des hives en majuscule : `SAM`, `SECURITY`, `SYSTEM`
- dans cette même colonne, la paramètre "ParentPID" apparait, avec la valeur `4176`

Hint : ne pas hésiter à ctl+f les mots clés connus : 'Hive', 'ruche', 'PID', 'Parent'

Flag : `CYBN{SAM_SECURITY_SYSTEM_4716}`