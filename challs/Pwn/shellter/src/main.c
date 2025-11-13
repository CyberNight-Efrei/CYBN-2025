#include <stdio.h>
#include <stdlib.h>

void shellter() {
    printf("GG, here's your shell-ter");
    system("/bin/sh");
}

void vuln() {
    char buffer[40];
    char leak[40];

    printf("I'll give you a little hint though, you can leak whatever you want from there\n> ");
    fgets(leak, 40, stdin);
    printf(leak);

    printf("Now go find your shell-ter\n> ");

    fgets(buffer, 0x80, stdin);
}

int main() {
    printf("Here a little medium intro to our beloved category, The infamous pwn.\nNow just find a shell-ter if you want to stay alive\n");
    vuln();
    printf("It looks like you didn't manage to find a shell-ter in time");
    exit(0);
}
