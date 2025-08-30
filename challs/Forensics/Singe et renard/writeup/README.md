`eq1sSFTiQKW6JeYj56IcqWVCpIxDvrawAW9+yTut+ZlrGvnJcHiDawHQV7laHtfV`

Part 1 :
- historique
- facebook
- autofill
- mettre un caractère dans mdp, puis retirer, ouvrir oeil
- mdp : `eq1sSFTiQKW6JeYj56IcqWVCpIxDvra`

Part 2 :
- historique
- cookies
- `FLAG_PART_2 : wAW9+yTut+ZlrGvnJcHiDawHQV7laHtfV`

Flag chiffré : `zvHKebC9t0yAgDOa7RxxLcgXzVv+gERawOL+ytI9hZs=`

Dans les extensions :
- violentmonkey
- script "Un flag ?"
- voir détail : https://chiffrer.info
- insérer `encryptedFlag = "zvHKebC9t0yAgDOa7RxxLcgXzVv+gERawOL+ytI9hZs="` 
- ouvrir le site
- profit : `CYBN{aM_I_cR4zy_H1dinG_S3Cret5_HER3?}`


Script : 
```js
// ==UserScript==
// @name        Un flag ?
// @namespace   Violentmonkey Scripts
// @match       https://chiffrer.info/
// @grant       none
// @version     1.0
// @author      me
// @require     https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.2.0/crypto-js.min.js
// ==/UserScript==

function encryptAES(text, password) {
    // Convertir la passphrase en un mot de passe utilisable
    let key = CryptoJS.enc.Utf8.parse(password);
    // Générer un IV à partir de la passphrase (pour la cohérence)
    let iv = CryptoJS.lib.WordArray.create(key.words.slice(0, 4));
    console.log("IV (Base64) : " + CryptoJS.enc.Base64.stringify(iv));

    // Chiffrement du texte
    var cipherText = CryptoJS.AES.encrypt(text, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });

    // Retourner le texte chiffré en Base64
    return cipherText.toString();
}

function decrypt(cipherText, password) {
  let key = CryptoJS.enc.Utf8.parse(password);
  let iv = CryptoJS.lib.WordArray.create(key.words.slice(0, 4));
  let ivBase64 = CryptoJS.enc.Base64.stringify(iv);

  let decrypted = CryptoJS.AES.decrypt(cipherText, key, {iv: iv,mode: CryptoJS.mode.CBC,padding: CryptoJS.pad.Pkcs7});

  return decrypted.toString(CryptoJS.enc.Utf8);
}

const passphrase = document.querySelector('h1.intro-text')?.textContent;

const encryptedFlag = encryptAES("CYBN{aM_I_cR4zy_H1dinG_S3Cret5_HER3?}", passphrase);
console.log(encryptedFlag)
const decryptedFlag = decrypt(encryptedFlag, passphrase);
console.log(decryptedFlag)
document.querySelector('header').innerHTML += `<div id="my-flag">${decryptedFlag}</div>`

const style = document.createElement('style');

style.textContent = `
  #my-flag {
    position: absolute;
    top: -20%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-image: linear-gradient(68.2deg, rgb(7, 3, 98) -0.1%, rgb(179, 26, 132) 47.7%, rgb(239, 186, 83) 100.2%);
    padding: 100px;
    animation: falling 7s ease forwards;
  }

  @keyframes falling {
    0% { top: -20% }
    100%  { top: 50vh; transform: translate(-50%, -50%) }
  }
`
document.head.appendChild(style);
```