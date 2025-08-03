#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/stat.h>
#include <time.h>
#include <openssl/aes.h>

void xor_decrypt(uint8_t *data, size_t len, uint8_t key) {
    for (size_t i = 0; i < len; i++)
        data[i] ^= key;
}

void rc4(uint8_t *data, size_t len, uint8_t *key, size_t keylen) {
    uint8_t S[256];
    for (int i = 0; i < 256; i++) S[i] = i;
    int j = 0;
    for (int i = 0; i < 256; i++) {
        j = (j + S[i] + key[i % keylen]) & 0xFF;
        uint8_t tmp = S[i]; S[i] = S[j]; S[j] = tmp;
    }

    int i = 0; j = 0;
    for (size_t n = 0; n < len; n++) {
        i = (i + 1) & 0xFF;
        j = (j + S[i]) & 0xFF;
        uint8_t tmp = S[i]; S[i] = S[j]; S[j] = tmp;
        uint8_t K = S[(S[i] + S[j]) & 0xFF];
        data[n] ^= K;
    }
}

void aes_decrypt(uint8_t *in, size_t len, uint8_t *key, uint8_t *iv, uint8_t **out, int *out_len) {
    AES_KEY aes_key;
    AES_set_decrypt_key(key, 128, &aes_key);

    *out = calloc(len, 1);
    memcpy(*out, in, len);

    AES_cbc_encrypt(*out, *out, len, &aes_key, iv, AES_DECRYPT);
    *out_len = len;

    uint8_t pad = (*out)[len - 1];
    if (pad > 0 && pad <= AES_BLOCK_SIZE)
        *out_len = len - pad;
}

void generate_key(uint8_t *buf, size_t len, unsigned int seed) {
    srand(seed);
    for (size_t i = 0; i < len; i++)
        buf[i] = rand() % 256;
}

time_t get_payload_timestamp(const char *filename) {
    struct stat st;
    if (stat(filename, &st) != 0) {
        perror("stat");
        exit(1);
    }
    return st.st_mtime;
}

int main() {
    const char *payload_file = "payload.out";
    FILE *f = fopen(payload_file, "rb");
    if (!f) {
        perror("fopen");
        return 1;
    }

    fseek(f, 0, SEEK_END);
    size_t len = ftell(f);
    fseek(f, 0, SEEK_SET);

    uint8_t *encrypted = malloc(len);
    if (!encrypted) {
        perror("malloc");
        fclose(f);
        return 1;
    }
    fread(encrypted, 1, len, f);
    fclose(f);

    time_t ts = get_payload_timestamp(payload_file);

    uint8_t xor_key;
    uint8_t rc4_key[4];
    uint8_t aes_key[16];
    uint8_t aes_iv[16];

    generate_key(&xor_key, 1, 0xC0FFEE + ts);
    generate_key(rc4_key, sizeof(rc4_key), 0xBEEF1337 + ts);
    generate_key(aes_key, sizeof(aes_key), 0xDEADBEEF + ts);
    generate_key(aes_iv, sizeof(aes_iv), 0x12345678 + ts);

    uint8_t *aes_out = NULL;
    int aes_len = 0;
    aes_decrypt(encrypted, len, aes_key, aes_iv, &aes_out, &aes_len);

    rc4(aes_out, aes_len, rc4_key, sizeof(rc4_key));
    xor_decrypt(aes_out, aes_len, xor_key);

    FILE *out = fopen("challenge.out", "wb");
    if (!out) {
        perror("fopen");
        free(encrypted);
        free(aes_out);
        return 1;
    }
    fwrite(aes_out, 1, aes_len, out);
    fclose(out);

    printf("[+] challenge.out written (%d bytes)\n", aes_len);

    free(encrypted);
    free(aes_out);
    return 0;
}