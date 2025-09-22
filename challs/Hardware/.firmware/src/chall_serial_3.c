#include <string.h>
#include <driver/uart.h>
#include <driver/gpio.h>

#include "chall_serial_3.h"

#define BUTTON (5)

#define RXD_PIN (18)
#define TXD_PIN (19)

static QueueHandle_t serial_3_evt_queue = NULL;

static void IRAM_ATTR serial_3_gpio_isr_handler(void *arg)
{
    uint32_t gpio_num = (uint32_t)arg;
    xQueueSendFromISR(serial_3_evt_queue, &gpio_num, NULL);
}

static void serial_3_task(void *arg)
{
    uint32_t io_num;
    for (;;)
    {
        if (xQueueReceive(serial_3_evt_queue, &io_num, portMAX_DELAY))
        {
            char *flag = "CYBN{th3_0dd_p4r1ty}\r\n";
            uart_write_bytes(UART_NUM_2, flag, strlen(flag));
            xQueueReset(serial_3_evt_queue);
        }
    }
}

void chall_serial_3(void)
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

    uart_config_t uart_config = {
        .baud_rate = 57600,
        .data_bits = UART_DATA_7_BITS,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .parity = UART_PARITY_ODD,
    };

    uart_param_config(UART_NUM_2, &uart_config);

    uart_set_pin(UART_NUM_2, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);

    uart_driver_install(UART_NUM_2, 512, 0, 0, NULL, 0);

    serial_3_evt_queue = xQueueCreate(10, sizeof(uint32_t));

    xTaskCreate(serial_3_task, "serial_3", 2048, NULL, 10, NULL);

    gpio_isr_handler_add(BUTTON, serial_3_gpio_isr_handler, NULL);
}
