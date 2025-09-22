#include <stdio.h>
#include <stdlib.h>

#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "gen_name.h"

#include "chall_serial_1.h"
#include "chall_serial_2.h"
#include "chall_serial_3.h"
#include "chall_morse.h"
#include "chall_ble.h"
#include "chall_wifi.h"

void app_main() {
    // esp_log_level_set("*", ESP_LOG_NONE);
    gen_name("CYBN-");
    // uart_set_baudrate(UART_NUM_0, 9600);

    gpio_install_isr_service(0);

    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND)
    {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    
    chall_serial_1();
    chall_serial_2();
    chall_serial_3();
    chall_morse();
    chall_ble();
    chall_wifi();
}
