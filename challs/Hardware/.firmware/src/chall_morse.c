#include <stdio.h>
#include <driver/gpio.h>
#include "freertos/FreeRTOS.h"

#include "morse.h"

#define BUTTON (4)

static QueueHandle_t morse_evt_queue = NULL;

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

    xTaskCreate(morse_task, "morse", 2048, NULL, 10, NULL);

    gpio_isr_handler_add(BUTTON, morse_gpio_isr_handler, NULL);
}
