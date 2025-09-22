#include <stdio.h>

#include "chall_serial_1.h"

void chall_serial_1(void)
{
    printf("\r\nBip bop, this message is sent from the ESP32!\r\n");
    printf("Well played on successfully connecting to the microcontroller, here is your flag:\r\n");
    printf("CYBN{serial_dot_println_is_the_way}\r\n");
    printf("\r\n\nPlease note that this console will be used for various logging.\r\n");
}
