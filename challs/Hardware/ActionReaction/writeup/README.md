Avec un simple sketch Arduino, on peut lire et envoyer des caractères pen série. Un test de niveau logique nous indique que le pin RX est le 16, et que le TX est le 17 (TX est en idle à HIGH). On envoie le caractère `y` au RX, et on obtient le flag.

Ainsi, avec ce sketch, en connectant 17 - 2 et 16 - 3 :
```c
#include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial Serial2(2, 3);

void setup() {
  Serial.begin(9600);
  Serial2.begin(9600);
}

void loop() {
  uint8_t c;
  if (Serial.available()) {
    Serial.readBytes(&c, 1);
    Serial2.write(c);
  }

  if (Serial2.available()) {
    Serial2.readBytes(&c, 1);
    Serial.write(c);
  }
}

```