#include <stdio.h>
#include <string.h>
#include <driver/uart.h>
#include <driver/gpio.h>

#include "chall_serial_2.h"

#define RXD_PIN (16)
#define TXD_PIN (17)

QueueHandle_t uart_queue;

static void chall_serial_2_task(void *pvParameters)
{
    uart_event_t event;
    char c;

    for (;;)
    {
        if (xQueueReceive(uart_queue, &event, portMAX_DELAY))
        {
            switch (event.type)
            {
            case UART_DATA:
                int len = uart_read_bytes(UART_NUM_1, &c, 1, pdMS_TO_TICKS(20));
                if (len > 0)
                {
                    uart_write_bytes(UART_NUM_1, &c, 1);
                    char *line_feed = "\r\n";
                    uart_write_bytes(UART_NUM_1, line_feed, 2);

                    if (c == 'y' || c == 'Y')
                    {
                        const char *flag = "CYBN{45ync_w1r3_tr4nsm15510n}\r\n";
                        uart_write_bytes(UART_NUM_1, flag, strlen(flag));
                    }
                    if (c == 'n' || c == 'N' || c == '\r' || c == '\n')
                    {
                        const char *msg_cancel = "Too bad :(\n\r";
                        uart_write_bytes(UART_NUM_1, msg_cancel, strlen(msg_cancel));
                    }
                    const char *msg = "Send the flag? [y/N] ";
                    uart_write_bytes(UART_NUM_1, msg, strlen(msg));
                }
                uart_flush_input(UART_NUM_1);
                xQueueReset(uart_queue);
                break;
            case UART_FIFO_OVF:
            case UART_BUFFER_FULL:
                uart_flush_input(UART_NUM_1);
                xQueueReset(uart_queue);
                break;
            default:
                break;
            }
        }
    }
}

void chall_serial_2(void)
{
    /**
     * Options pour l'UART
     * Pour pimenter, mettre UART_PARITY_ODD / EVEN,
     * ou + de bits de stop
     */
    uart_config_t uart_config = {
        .baud_rate = 9600,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };
    
    uart_param_config(UART_NUM_1, &uart_config);

    uart_set_pin(UART_NUM_1, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);

    uart_driver_install(UART_NUM_1, 512, 512, 10, &uart_queue, 0);

    const char *msg = "Send the flag? [y/N] ";
    uart_write_bytes(UART_NUM_1, msg, strlen(msg));

    xTaskCreate(chall_serial_2_task, "chall_serial_2", 2048, NULL, 12, NULL);
}
