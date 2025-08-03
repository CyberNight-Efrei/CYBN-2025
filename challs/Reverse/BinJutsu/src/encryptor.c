#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <time.h>
#include <sys/ptrace.h>
#include <openssl/aes.h>

void xor_encrypt(uint8_t *data, size_t len, uint8_t key) {
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

    int i = 0;
    j = 0;
    for (size_t n = 0; n < len; n++) {
        i = (i + 1) & 0xFF;
        j = (j + S[i]) & 0xFF;
        uint8_t tmp = S[i]; S[i] = S[j]; S[j] = tmp;
        uint8_t K = S[(S[i] + S[j]) & 0xFF];
        data[n] ^= K;
    }
}

void aes_encrypt(uint8_t *data, size_t len, uint8_t *key, uint8_t *iv, uint8_t **out, int *out_len) {
    AES_KEY aes_key;
    AES_set_encrypt_key(key, 128, &aes_key);

    int padded_len = ((len + AES_BLOCK_SIZE) / AES_BLOCK_SIZE) * AES_BLOCK_SIZE;
    *out = calloc(padded_len, 1);
    if (!*out) {
        perror("calloc");
        exit(1);
    }

    memcpy(*out, data, len);
    uint8_t pad = padded_len - len;
    for (size_t i = len; i < padded_len; i++) (*out)[i] = pad;

    AES_cbc_encrypt(*out, *out, padded_len, &aes_key, iv, AES_ENCRYPT);
    *out_len = padded_len;
}

void write_payload_binary(uint8_t *buf, int len, const char *filename) {
    FILE *f = fopen(filename, "wb");
    if (!f) {
        perror("fopen");
        exit(1);
    }

    fwrite(buf, 1, len, f);
    fclose(f);
}

int is_debugger_present() {
    if (ptrace(PTRACE_TRACEME, 0, NULL, 0) == -1)
        return 1;
    ptrace(PTRACE_DETACH, 0, NULL, 0);
    return 0;
}

void generate_key(uint8_t *buf, size_t len, unsigned int seed) {
    time_t now = time(NULL);
    srand(seed + (unsigned int)now);
    for (size_t i = 0; i < len; i++)
        buf[i] = rand() % 256;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <input-binary>\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        perror("fopen");
        return 1;
    }
    fseek(f, 0, SEEK_END);
    size_t len = ftell(f);
    fseek(f, 0, SEEK_SET);
    uint8_t *buf = malloc(len);
    if (!buf) {
        perror("malloc");
        fclose(f);
        return 1;
    }
    fread(buf, 1, len, f);
    fclose(f);

    int debug = is_debugger_present();
    uint8_t xor_key;
    uint8_t rc4_key[4];
    uint8_t aes_key[16];
    uint8_t aes_iv[16];

    if (!debug) {
        generate_key(&xor_key, 1, 0xC0FFEE);
        generate_key(rc4_key, sizeof(rc4_key), 0xBEEF1337);
        generate_key(aes_key, sizeof(aes_key), 0xDEADBEEF);
        generate_key(aes_iv, sizeof(aes_iv), 0x12345678);
    } else {
        xor_key = 0x7A;
        uint8_t tmp_rc4[] = { 0x4F, 0x22, 0x91, 0x7C };
        memcpy(rc4_key, tmp_rc4, sizeof(tmp_rc4));
        uint8_t tmp_aes_key[16] = {
            0x9C, 0x1F, 0x7D, 0x8A,
            0x26, 0xB3, 0x5D, 0xE2,
            0x47, 0x90, 0x3B, 0x0C,
            0xD8, 0xA1, 0xE3, 0x76
        };
        memcpy(aes_key, tmp_aes_key, sizeof(tmp_aes_key));
        uint8_t tmp_iv[16] = {
            0xA5, 0xC4, 0xE2, 0x6B,
            0xF1, 0x29, 0x87, 0xD2,
            0x55, 0x6F, 0x93, 0x20,
            0x14, 0x37, 0x4C, 0x8D
        };
        memcpy(aes_iv, tmp_iv, sizeof(tmp_iv));
    }

    xor_encrypt(buf, len, xor_key);
    rc4(buf, len, rc4_key, sizeof(rc4_key));

    uint8_t *encrypted;
    int encrypted_len;
    aes_encrypt(buf, len, aes_key, aes_iv, &encrypted, &encrypted_len);

    write_payload_binary(encrypted, encrypted_len, "payload.out");
    printf("[+] payload.out written successfully (%d bytes)\n", encrypted_len);

    free(buf);
    free(encrypted);
    return 0;
}