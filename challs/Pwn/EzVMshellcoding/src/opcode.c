#include "opcode.h"
#include <stdio.h>
#include "syscall.h"


int valueFromReg(enum Registers_e reg){
    int value;
    switch (reg){
        case R1:
            value = r1.reg_value;
            break;
        case R2:
            value = r2.reg_value;
            break;
        case R3:
            value = r3.reg_value;
            break;
        case R4:
            value = r4.reg_value;
            break;
        case R5:
            value = r5.reg_value;
            break;
        case R6:
            value = r6.reg_value;
            break;
        case RET:
            value = ret.reg_value;
            break;
        case IP:
            value = ip.reg_value;
            break;
        case SP:
            value = sp.reg_value;
            break;
        default:
            value = 0;
            break;
    }
    return value;
}

void pushd(int value){
    STACK[sp.reg_value++] = value;
}

void push(enum Registers_e reg){
    int value;
    if (reg != IP && reg != SP){
        value = valueFromReg(reg);
        pushd(value);
    }
}

void pop(){
    ret.reg_value = STACK[--sp.reg_value];
}

void add_direct(enum Registers_e reg1, int val){
    switch (reg1){
        case R1:
            r1.reg_value += val;
            break;
        case R2:
            r2.reg_value += val;
            break;
        case R3:
            r3.reg_value += val;
            break;
        case R4:
            r4.reg_value += val;
            break;
        case R5:
            r5.reg_value += val;
            break;
        case R6:
            r6.reg_value += val;
            break;
        case RET:
            ret.reg_value += val;
            break;
        case IP:
            ip.reg_value += val;
            break;
        case SP:
            sp.reg_value += val;
            break;
        default:
            return;
    }
    return;
}

void add(enum Registers_e reg1, enum Registers_e reg2){
    int value;
    value = valueFromReg(reg2);
    add_direct(reg1,value);
}

void sub_direct(enum Registers_e reg1, int val){
    switch (reg1){
        case R1:
            r1.reg_value -= val;
            break;
        case R2:
            r2.reg_value -= val;
            break;
        case R3:
            r3.reg_value -= val;
            break;
        case R4:
            r4.reg_value -= val;
            break;
        case R5:
            r5.reg_value -= val;
            break;
        case R6:
            r6.reg_value -= val;
            break;
        case RET:
            ret.reg_value -= val;
            break;
        case IP:
            ip.reg_value -= val;
            break;
        case SP:
            sp.reg_value -= val;
            break;
        default:
            return;
    }
    return;

}

void sub(enum Registers_e reg1, enum Registers_e reg2){
    int value;
    value = valueFromReg(reg2);
    sub_direct(reg1,value);
}

void mov_direct(enum Registers_e reg1, int val){
    switch (reg1){
        case R1:
            r1.reg_value = val;
            break;
        case R2:
            r2.reg_value = val;
            break;
        case R3:
            r3.reg_value = val;
            break;
        case R4:
            r4.reg_value = val;
            break;
        case R5:
            r5.reg_value = val;
            break;
        case R6:
            r6.reg_value = val;
            break;
        case RET:
            ret.reg_value = val;
            break;
        case IP:
            ip.reg_value = val;
            break;
        case SP:
            sp.reg_value = val;
            break;
        default:
            return;
    }
    return;
}

void mov(enum Registers_e reg1, enum Registers_e reg2){
    int value;
    value = valueFromReg(reg2);
    mov_direct(reg1,value);
}

void mul_direct(enum Registers_e reg1, int val){
    switch (reg1){
        case R1:
            r1.reg_value *= val;
            break;
        case R2:
            r2.reg_value *= val;
            break;
        case R3:
            r3.reg_value *= val;
            break;
        case R4:
            r4.reg_value *= val;
            break;
        case R5:
            r5.reg_value *= val;
            break;
        case R6:
            r6.reg_value *= val;
            break;
        case RET:
            ret.reg_value *= val;
            break;
        case IP:
            ip.reg_value *= val;
            break;
        case SP:
            sp.reg_value *= val;
            break;
        default:
            return;
    }
    return;
}

void mul(enum Registers_e reg1, enum Registers_e reg2){
    int value;
    value = valueFromReg(reg2);
    mul_direct(reg1,value);
}

void cmp(){
    ret.reg_value = (r1.reg_value == r2.reg_value);
}

void print(){
    printf("%s", &STACK[sp.reg_value]);
}


int opcode_dispatcher(char op){
    int ret_code = 0;
    int value;
    enum Registers_e reg1, reg2;
    switch (op){
        case MOV:
            reg1 = CODE[ip.reg_value++];
            reg2 = CODE[ip.reg_value++];
            mov(reg1, reg2);
            break;
        case MOVI:
            reg1 = CODE[ip.reg_value++];
            value = CODE[ip.reg_value++];
            if (value < 32 || value > 127) return -1;
            mov_direct(reg1, value);
            break;
        case PUSH:
            reg1 = CODE[ip.reg_value++];
            push(reg1);
            break;
        case PUSHD:
            value = CODE[ip.reg_value++];
            if (value < 32 || value > 127) return -1;
            pushd(value);
            break;
        case POP:
            pop();
            break;
        case ADD:
            reg1 = CODE[ip.reg_value++];
            reg2 = CODE[ip.reg_value++];
            add(reg1, reg2);
            break;
        case ADDI:
            reg1 = CODE[ip.reg_value++];
            value = CODE[ip.reg_value++];
            if (value < 32 || value > 127) return -1;
            add_direct(reg1, value);
            break;
        case SUB:
            reg1 = CODE[ip.reg_value++];
            reg2 = CODE[ip.reg_value++];
            sub(reg1, reg2);
            break;
        case SUBI:
            reg1 = CODE[ip.reg_value++];
            value = CODE[ip.reg_value++];
            if (value < 32 || value > 127) return -1;
            sub_direct(reg1, value);
            break;
        case MUL:
            reg1 = CODE[ip.reg_value++];
            reg2 = CODE[ip.reg_value++];
            mul(reg1, reg2);
            break;
        case MULI:
            reg1 = CODE[ip.reg_value++];
            value = CODE[ip.reg_value++];
            if (value < 32 || value > 127) return -1;
            mul_direct(reg1, value);
            break;
        case CMP:
            cmp();
            break;
        case PRINT:
            print();
            break;
        case SYS:
            syscall_dispatcher(CODE[ip.reg_value++]);
            break;
        case END:
            ret_code = 1;
            break;
        default:
            ret_code = 2;
            break;
    }
    return ret_code;
}

