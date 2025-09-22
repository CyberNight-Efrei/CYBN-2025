#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"
#include "esp_log.h"
#include "nimble/nimble_port.h"
#include "nimble/nimble_port_freertos.h"
#include "host/ble_hs.h"
#include "host/ble_uuid.h"
#include "host/ble_gatt.h"
#include "services/gap/ble_svc_gap.h"
#include "services/gatt/ble_svc_gatt.h"

#include "gen_name.h"

static const char *TAG = "chall_ble";
static uint8_t ble_addr_type;

static const char flag_value[] = "CYBN{unencrypted_communication_baby}";

static void ble_app_on_sync(void);
static void ble_app_on_reset(int reason);
static int gap_event_handler(struct ble_gap_event *event, void *arg);
static int gatt_svc_init(void);
static void host_task(void *param);
static void ble_app_advertise(void);

static int flag_access_cb(uint16_t conn_handle, uint16_t attr_handle,
                          struct ble_gatt_access_ctxt *ctxt, void *arg)
{
    (void)conn_handle;
    (void)attr_handle;
    (void)arg;

    if (ctxt->op == BLE_GATT_ACCESS_OP_READ_CHR)
    {
        int rc = os_mbuf_append(ctxt->om, flag_value, strlen(flag_value));
        if (rc != 0)
        {
            ESP_LOGE(TAG, "os_mbuf_append failed rc=%d", rc);
            return BLE_ATT_ERR_INSUFFICIENT_RES;
        }
        return 0; /* success */
    }

    return BLE_ATT_ERR_UNLIKELY;
}

static const struct ble_gatt_svc_def gatt_svr_svcs[] = {
    {.type = BLE_GATT_SVC_TYPE_PRIMARY,
     .uuid = BLE_UUID16_DECLARE(0xFF10),
     .characteristics = (struct ble_gatt_chr_def[]){
         {
             .uuid = BLE_UUID16_DECLARE(0xFF11),
             .access_cb = flag_access_cb,
             .flags = BLE_GATT_CHR_F_READ,
         },
         {0}}},
    {0}};

static int gatt_svc_init(void)
{
    int rc;

    ble_svc_gatt_init();

    rc = ble_gatts_count_cfg(gatt_svr_svcs);
    if (rc != 0)
    {
        ESP_LOGE(TAG, "ble_gatts_count_cfg failed rc=%d", rc);
        return rc;
    }

    rc = ble_gatts_add_svcs(gatt_svr_svcs);
    if (rc != 0)
    {
        ESP_LOGE(TAG, "ble_gatts_add_svcs failed rc=%d", rc);
        return rc;
    }

    ESP_LOGI(TAG, "GATT services added");
    return 0;
}

static int gap_event_handler(struct ble_gap_event *event, void *arg)
{
    switch (event->type)
    {
    case BLE_GAP_EVENT_CONNECT:
        if (event->connect.status == 0)
        {
            ESP_LOGI(TAG, "Connection established\n");
        }
        else
        {
            ESP_LOGW(TAG, "Connection failed; status=%d\n", event->connect.status);
            ble_app_advertise();
        }
        break;

    case BLE_GAP_EVENT_DISCONNECT:
        ESP_LOGI(TAG, "Disconnected; reason=%d\n", event->disconnect.reason);
        ble_app_advertise();
        break;

    default:
        break;
    }

    return 0;
}

static void ble_app_advertise(void)
{
    struct ble_gap_adv_params adv_params;
    struct ble_hs_adv_fields fields;
    int rc;

    memset(&fields, 0, sizeof(fields));

    fields.flags = BLE_HS_ADV_F_DISC_GEN | BLE_HS_ADV_F_BREDR_UNSUP;

    fields.name = (uint8_t *)esp_name;
    fields.name_len = strlen(esp_name);
    fields.name_is_complete = 1;

    fields.tx_pwr_lvl_is_present = 1;

    rc = ble_gap_adv_set_fields(&fields);
    if (rc != 0)
    {
        ESP_LOGE(TAG, "ble_gap_adv_set_fields failed rc=%d", rc);
        return;
    }

    memset(&adv_params, 0, sizeof(adv_params));
    adv_params.conn_mode = BLE_GAP_CONN_MODE_UND;
    adv_params.disc_mode = BLE_GAP_DISC_MODE_GEN;

    rc = ble_gap_adv_start(ble_addr_type, NULL, BLE_HS_FOREVER,
                           &adv_params, gap_event_handler, NULL);
    if (rc != 0)
    {
        ESP_LOGE(TAG, "ble_gap_adv_start failed rc=%d", rc);
    }
    else
    {
        ESP_LOGI(TAG, "Advertising started");
    }
}

static void ble_app_on_sync(void)
{
    int rc;

    rc = ble_hs_id_infer_auto(0, &ble_addr_type);
    if (rc != 0)
    {
        ESP_LOGE(TAG, "ble_hs_id_infer_auto failed rc=%d", rc);
        return;
    }

    ble_svc_gap_device_name_set(esp_name);

    ble_app_advertise();
}

static void ble_app_on_reset(int reason)
{
    ESP_LOGE(TAG, "NimBLE reset; reason=%d", reason);
}

static void host_task(void *param)
{
    ESP_LOGI(TAG, "NimBLE host task started");
    nimble_port_run();
    nimble_port_freertos_deinit();
}

void chall_ble(void)
{
    int rc;

    nimble_port_init();

    ble_hs_cfg.reset_cb = ble_app_on_reset;
    ble_hs_cfg.sync_cb = ble_app_on_sync;

    rc = gatt_svc_init();
    if (rc != 0)
    {
        ESP_LOGE(TAG, "gatt_svc_init failed rc=%d", rc);
    }

    nimble_port_freertos_init(host_task);
}
