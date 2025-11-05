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

    // Challenge Pull Up! Pull Up!
    // level == 1 -> switch sur la position "ch1"
    if (level == 1)
    {
        print("CYBN{" FLAG_CHALL_PULL_UP "}");

        // Boucle infinie
        for (;;) asm volatile ("nop");
    }
    // Challenge No Time To Flag
    else
    {
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
    }

    return 0;
}
