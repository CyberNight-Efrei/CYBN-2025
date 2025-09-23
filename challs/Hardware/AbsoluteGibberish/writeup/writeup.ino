#include <EEPROM.h>

uint8_t options[] = {
    SERIAL_7N1,
    SERIAL_8N1,
    SERIAL_7N2,
    SERIAL_8N2,
    SERIAL_7E1,
    SERIAL_8E1,
    SERIAL_7E2,
    SERIAL_8E2,
    SERIAL_7O1,
    SERIAL_8O1,
    SERIAL_7O2,
    SERIAL_8O2,
};

int options_length = 12;

unsigned long baud_rates[] = {
    50,
    75,
    110,
    134,
    150,
    200,
    300,
    600,
    1200,
    1800,
    2400,
    4800,
    9600,
    19200,
    28800,
    38400,
    57600,
    76800,
    115200,
};

#ifndef READING
#define TIMEOUT 1000

int baud_rates_length = 19;
char recieved[5];
char check[] = "CYBN{";

uint8_t o;
uint8_t b;

bool success = false;

void setup()
{
    pinMode(2, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
    for (o = 0; o < options_length; o++)
    {
        for (b = 0; b < baud_rates_length; b++)
        {
            bool s = true;
            Serial.begin(baud_rates[b], options[o]);

            digitalWrite(2, HIGH);
            delay(1);
            digitalWrite(2, LOW);

            unsigned long m = millis();
            while (Serial.available() < 5 && (millis() - m < TIMEOUT))
                ;
            if (Serial.available() < 5)
            {
                s = false;
            }
            else
            {
                Serial.readBytes(recieved, 5);
                for (int i = 0; i < 5; i++)
                {
                    if (check[i] != recieved[i])
                    {
                        s = false;
                    }
                }
            }
            if (s == true)
            {
                EEPROM.put(0, o);
                EEPROM.put(1, b);
                success = true;
                return;
            }
            Serial.end();
            delay(100);
        }
    }
}

void loop()
{
    int d = 500;
    if (success == false)
    {
        d = 100;
    }
    digitalWrite(LED_BUILTIN, HIGH);
    delay(d);
    digitalWrite(LED_BUILTIN, LOW);
    delay(d);
}

#else

uint8_t o;
uint8_t b;

void setup()
{
    Serial.begin(9600);
    EEPROM.get(0, o);
    EEPROM.get(1, b);

    Serial.print("baud rate a ");
    Serial.print(baud_rates[b]);
    Serial.print(", option numero ");
    Serial.println(o);
}

void loop()
{
}

#endif
