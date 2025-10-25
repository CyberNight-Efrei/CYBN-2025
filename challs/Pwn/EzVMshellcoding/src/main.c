#include "opcode.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>

char CODE[110] = {0};
char STACK[200] = {0};
my_register_t sp = {"sp", 0}; // between 0 and 10000 theoretically
my_register_t ip = {"ip", 0}; // between 0 and size of code theoretically
my_register_t r1 = {"r1", 0};
my_register_t r2 = {"r2", 0};
my_register_t r3 = {"r3", 0};
my_register_t r4 = {"r4", 0};
my_register_t r5 = {"r5", 0};
my_register_t r6 = {"r6", 0};
my_register_t ret = {"ret", 0};

int load_code() { // for test but will need a function for reading the real input
    FILE *file;

    // Open the binary file for reading
    file = fopen("shellcode.bin", "rb");
    if(file == NULL) {
        perror("Error opening file");
        return 1;
    }

    // read the shellcode into CODE
    fread(CODE, sizeof(char), 90, file);

    fclose(file);
    return 0;
}

int get_input() {
    printf("Welcome to this fake vm pwn chall\n");
    printf("Don't worry it's easy\n>> ");

    fgets(CODE, 90, stdin);

    printf("\nNow let's run it : ");

    return 0;
}

int main() {
    // load_code();
    get_input();

    int end = 0;
    char curinstr;
    while(end == 0) {
        curinstr = CODE[ip.reg_value++];
        end = opcode_dispatcher(curinstr);
    }
    if(end == -1) {
        printf("NOPE you aren't allowed this (but i won't tell you what)");
    }
    return 0;
}

// intended solve
// B/BpBrBoBcB/BsBeBlBfB/BrBoBoBtB/BfBlBaBgEB0BrIEDTBHDPHBEIF!IP0GP0TCS
// will be compiled with -m32 only
