#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void xor_string(const char *input, char *output) {
    size_t len = strlen(input);

    for (size_t i = 0; i < len; i++) {
        output[i] = input[i] ^ (char) 0x69;
    }

    output[len] = '\0';
}

int main() {
    const char *instruction_path = "/tmp/instruction.txt";
    const char *flag_path = "/tmp/flag";
    const char *target = "give me the flag";

    char buffer[1024];

    FILE *fp = fopen(instruction_path, "r");
    if (fp == NULL) {
        printf("Unknown instructions.\n");
        return 1;
    }

    size_t read_size = fread(buffer, 1, sizeof(buffer) - 1, fp);
    buffer[read_size] = '\0';
    fclose(fp);

    if (strstr(buffer, target) != NULL) {
        FILE *out = fopen(flag_path, "w");
        if (out == NULL) {
            perror("Could not open flag file for writing");

            return 1;
        }

        const char encoded[] = { 0x2a, 0x30, 0x2b, 0x27, 0x12, 0x2d, 0x5a, 0x0a, 0x1b, 0x10, 0x19, 0x1d, 0x58, 0x07, 0x0e, 0x36, 0x5d, 0x07, 0x0d, 0x36, 0x5a, 0x11, 0x5a, 0x0a, 0x1c, 0x1d, 0x58, 0x07, 0x0e, 0x36, 0x58, 0x07, 0x36, 0x24, 0x5a, 0x04, 0x59, 0x1b, 0x10, 0x36, 0x58, 0x1a, 0x36, 0x3a, 0x3c, 0x3a, 0x14 };
        const int encoded_len = sizeof(encoded) / sizeof(encoded[0]);

        char decoded[encoded_len + 1];

        xor_string(encoded, decoded);

        fprintf(out, "%s\n", decoded);
        fclose(out);
        printf("Flag written to %s\n", flag_path);
    } else {
        printf("Unknown instructions.\n");
    }

    return 0;
}

