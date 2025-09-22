#ifndef MORSE_H
#define MORSE_H

#include "driver/gpio.h"

extern const char morse_alphabet[];
extern const char *morse_translation[];

void send_morse_letter(char);
void send_morse_string(const char *);
void morse_setup(gpio_num_t pin, int base_delay);

#endif