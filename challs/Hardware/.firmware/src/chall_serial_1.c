#include <stdio.h>
#include "gen_name.h"

#include "chall_serial_1.h"

void chall_serial_1(void)
{
    printf("\r\nBip bop, ce message est envoyé depuis l'ESP32!\r\n");
    printf("Bien joué, tu as réussi à te connecter au microcontrolleur, voici ton flag :\r\n");
    printf("CYBN{serial_dot_println_is_the_way}\r\n");
    printf("\r\n\nLe nom de ce microcontrolleur est %s\r\n", esp_name);
}
