#include <stdio.h>
#include "esp_mac.h"
#include "gen_name.h"

char esp_name[32];

void gen_name(const char *pre)
{
    uint8_t mac[6];
    esp_read_mac(mac, ESP_MAC_WIFI_STA);
    snprintf(esp_name, sizeof(esp_name), "%s%02X%02X", pre, mac[0], mac[1]);
}
