#include <stdio.h>
#include <stdlib.h>
#include <string.h>

const char BASE64[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

void base64_encode(const char *in, const unsigned long in_len, char *out) {
    int in_index = 0;
    int out_index = 0;

    while (in_index < in_len) {
        out[out_index++] = BASE64[(in[in_index] & 0xFC) >> 2];

        if ((in_index + 1) == in_len) {
            out[out_index++] = BASE64[((in[in_index] & 0x3) << 4)];
            out[out_index++] = '=';
            out[out_index++] = '=';
            break;
        }

        out[out_index++] = BASE64[((in[in_index] & 0x3) << 4) | ((in[in_index + 1] & 0xF0) >> 4)];

        if ((in_index + 2) == in_len) {
            out[out_index++] = BASE64[((in[in_index + 1] & 0xF) << 2)];
            out[out_index++] = '=';
            break;
        }

        out[out_index++] = BASE64[((in[in_index + 1] & 0xF) << 2) | ((in[in_index + 2] & 0xC0) >> 6)];
        out[out_index++] = BASE64[in[in_index + 2] & 0x3F];

        in_index += 3;
    }

    out[out_index] = '\0';
}

void join_chunks(char *dest, const char **chunks, int count) {
    dest[0] = '\0';
    for (int i = 0; i < count; i++) {
        strcat(dest, chunks[i]);
    }
}

int main(int argc, char *argv[]) {
    const char *chunks[] = {
        "Q1lC", "Tntu", "MFRf", "UzBf",
        "SDRy", "RF90", "MF9G", "MW5E",
        "X0h1", "SH0="
    };
    char expected_b64[128];

    join_chunks(expected_b64, chunks, sizeof(chunks) / sizeof(chunks[0]));

    if (argc == 2) {
        char encoded[256];
        base64_encode(argv[1], strlen(argv[1]), encoded);

        if (strcmp(encoded, expected_b64) == 0) {
            printf("Yay\n");
        } else {
            printf("Nay\n");
        }
    } else {
        printf("Nothing to see here.\n");
    }

    return 0;
}