#include <stdio.h>
#include <string.h>
#include <stdint.h>

#define XOR_KEY 0x42

const uint8_t encrypted_password[] = {
    0x01, 0x1B, 0x00, 0x0C, 0x39, 0x75, 0x2A, 0x76,
    0x36, 0x1D, 0x15, 0x76, 0x31, 0x1D, 0x11, 0x72,
    0x0F, 0x71, 0x1D, 0x21, 0x72, 0x72, 0x2E, 0x1D,
    0x00, 0x73, 0x2C, 0x08, 0x37, 0x75, 0x11, 0x37,
    0x3F
};
const size_t password_len = 33;

int main() {
    char input[128];
    printf("Enter password: ");
    fgets(input, sizeof(input), stdin);

    size_t len = strcspn(input, "\n");
    input[len] = '\0';

    if (strlen(input) != password_len) {
        printf("NOPE\n");
        return 0;
    }

    char decrypted[128];
    for (size_t i = 0; i < password_len; i++) {
        decrypted[i] = encrypted_password[i] ^ XOR_KEY;
    }

    if (memcmp(input, decrypted, password_len) == 0) {
        printf("OK\n");
    } else {
        printf("NOPE\n");
    }

    return 0;
}