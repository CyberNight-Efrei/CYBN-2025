#include <Arduino.h>
#include "secret.h"

#define FLAG "CYBN{" SECRET_PASSWORD "}"
#define BUTTON_PIN (5)
#define RX_PIN (18)
#define TX_PIN (19)

int b_state = 0;
int b_prev_state = 0;

void setup()
{
    Serial.begin(SECRET_BAUD_RATE, SECRET_OPTION, RX_PIN, TX_PIN);
    pinMode(BUTTON_PIN, INPUT);
}

void loop()
{
    b_state = digitalRead(BUTTON_PIN);
    if (b_state && !(b_prev_state))
    {
        Serial.println(FLAG)
    }
    b_prev_state = b_state;
}
