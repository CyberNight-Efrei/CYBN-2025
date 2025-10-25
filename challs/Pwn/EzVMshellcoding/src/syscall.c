#include "syscall.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void sysopen(){
    // condition on OPEN is that it needs to contains 1 of the first level directory /etc, /proc etc (args : r1=path address, r2=mode address (will read everything on the stack), ret=0)
    if (ret.reg_value!=0){
        return;
    }
    char *path = &STACK[r1.reg_value];
    if (!(strstr(path, "/etc")!=NULL || strstr(path, "/proc")!=NULL || strstr(path, "/dev")!=NULL || strstr(path, "/tmp")!=NULL || strstr(path, "/home")!=NULL || strstr(path, "/mnt")!=NULL)){
        return;
    }
    char *mode = &STACK[r2.reg_value];
    ret.reg_value = (intptr_t)fopen(path, mode);
}

void sysread(){
    // condition on READ is that bufaddress must be greater than count (args : r1=fd, r2=buf address in terms of STACK, r3=count, ret=0)
    if (ret.reg_value!=0){
        return;
    }
    if (r2.reg_value < r3.reg_value) return;
    FILE *file = (FILE *)r1.reg_value;
    fread(&STACK[r2.reg_value],sizeof(char),r3.reg_value,file);
    return;
}

void syscall_dispatcher(char op){
    switch(op){
        case READ:
            sysread();
            break;
        case OPEN:
            sysopen();
            break;
        default:
            break;
    }
}
