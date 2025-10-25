#ifndef SYSCALL_H
#define SYSCALL_H
#include "opcode.h"

enum Syscall_e {
    OPEN = 0x42, // condition on OPEN is that it needs to contains 1 of the first level directory /etc, /proc etc (args : r1=path address, r2=mode address (will read everything on the stack), ret=0)
    READ = 0x43, // condition on READ is that bufaddress must be greater than count (args : r1=fd, r2=buf address in terms of STACK, r3=count, ret=0)
};

void sysopen();
void sysread();
void syscall_dispatcher(char op);

#endif
