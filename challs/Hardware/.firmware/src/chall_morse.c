#include <stdio.h>
#include <driver/gpio.h>
#include "freertos/FreeRTOS.h"
#include "esp_log.h"

#define BUTTON (4)

char *TAG = "chall_morse";

static QueueHandle_t morse_evt_queue = NULL;

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

static void IRAM_ATTR morse_gpio_isr_handler(void *arg)
{
    uint32_t gpio_num = (uint32_t)arg;
    xQueueSendFromISR(morse_evt_queue, &gpio_num, NULL);
}

static void morse_task(void *args)
{
    uint32_t io_num;
    for (;;)
    {
        if (xQueueReceive(morse_evt_queue, &io_num, portMAX_DELAY))
        {
            ESP_LOGI(TAG, "Button pulled up, sending morse text");
            char *msg = "sos mayday the flag is m0rs3isaw3s0me";
            printf("Transmitting on pin 2...\r\n");
            send_morse_string(msg);
            printf("Done\r\n");
            xQueueReset(morse_evt_queue);
        }
    }
}

void chall_morse(void)
{
    // Configure pin
    gpio_config_t io_conf = {
        .intr_type = GPIO_INTR_POSEDGE, // rising edge
        .mode = GPIO_MODE_INPUT,        // input
        .pin_bit_mask = (1ULL << BUTTON),
        .pull_down_en = GPIO_PULLDOWN_ENABLE, // enable pulldown
        .pull_up_en = GPIO_PULLUP_DISABLE
    };

    gpio_config(&io_conf);
    morse_setup(2, 100);

    morse_evt_queue = xQueueCreate(10, sizeof(uint32_t));

    xTaskCreate(morse_task, TAG, 2048, NULL, 10, NULL);

    gpio_isr_handler_add(BUTTON, morse_gpio_isr_handler, NULL);
}
