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