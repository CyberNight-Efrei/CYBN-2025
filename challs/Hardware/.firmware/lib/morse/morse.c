#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "driver/gpio.h"
#include "morse.h"

const char morse_alphbet[] = "abcdefghijklmnopqrstuvwxyz0123456789.,?";

const char *morse_translation[] = {
    ".-",
    "-...",
    "-.-.",
    "-..",
    ".",
    "..-.",
    "--.",
    "....",
    "..",
    ".---",
    "-.-",
    ".-..",
    "--",
    "-.",
    "---",
    ".--.",
    "--.-",
    ".-.",
    "...",
    "-",
    "..-",
    "...-",
    ".--",
    "-..-",
    "-.--",
    "--..",
    "-----",
    ".----",
    "..---",
    "...--",
    "....-",
    ".....",
    "-....",
    "--...",
    "---..",
    "----.",
    ".-.-.-",
    "--..--",
    "..--.."
};

static int short_delay = 0;
static int long_delay = 0;
static gpio_num_t out_pin = 0;


void send_morse_letter(char c)
{
    if (c == ' ')
    {
        vTaskDelay(pdMS_TO_TICKS(long_delay));
        vTaskDelay(pdMS_TO_TICKS(short_delay));
        return;
    }

    int i = 0;
    while (i < 40 && morse_alphbet[i] != c)
        i++;
    if (i == 40)
        return;

    const char *morse_code = morse_translation[i];
    while ((*morse_code) != 0)
    {
        gpio_set_level(out_pin, 1);
        // send dot
        if ((*morse_code++) == '.')
        {
            vTaskDelay(pdMS_TO_TICKS(short_delay));
        }
        // send dash
        else
        {
            vTaskDelay(pdMS_TO_TICKS(long_delay));
        }
        gpio_set_level(out_pin, 0);
        vTaskDelay(pdMS_TO_TICKS(short_delay));
    }
    vTaskDelay(pdMS_TO_TICKS(short_delay));
    vTaskDelay(pdMS_TO_TICKS(short_delay));
    return;
}

void send_morse_string(const char *s)
{
    while(*s != 0)
    {
        send_morse_letter(*s++);
    }
}

void morse_setup(gpio_num_t pin, int base_delay)
{
    out_pin = pin;

    gpio_config_t io_conf = {
        .pin_bit_mask = (1ULL << pin),
        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE,
    };

    gpio_config(&io_conf);

    gpio_set_level(pin, 0);

    short_delay = base_delay;
    long_delay = base_delay * 3;
}

