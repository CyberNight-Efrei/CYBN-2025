#ifndef OPCODE_H
#define OPCODE_H

enum OpCodes {
    PUSH = 0x41,  // push from reg
    PUSHD = 0x42, // push from direct value
    POP = 0x43,   // pop into register ret
    ADD = 0x44,   // add reg2 to reg1
    ADDI = 0x45,  // add directly integer into reg1
    SUB = 0x46,   // substract reg2 to reg1
    SUBI = 0x47,  // substract integer to reg1
    MOV = 0x48,   // mov reg2 value to reg1
    MOVI = 0x49,  // mov integer to reg1
    MUL = 0x50,   // multiply reg1 by reg2
    MULI = 0x51,  // multiply reg1 by integer
    CMP = 0x52,   // compare reg r1 and r2 and store result in ret
    PRINT = 0x53, // printf("%s") from the stack
    SYS = 0x54,   // call the syscall dispatcher
    END = 0x55,   // make the vm end
};

struct register_s {
    char *reg_name;
    int reg_value;
};
typedef struct register_s my_register_t;

enum Registers_e {
    SP = 0x42,
    IP = 0x43,
    R1 = 0x44,
    R2 = 0x45,
    R3 = 0x46,
    R4 = 0x47,
    R5 = 0x48,
    R6 = 0x49,
    RET = 0x50,
};

extern char CODE[110];
extern char STACK[200];

extern my_register_t sp; // between 0 and 10000 theoretically
extern my_register_t ip; // between 0 and size of code theoretically
extern my_register_t r1;
extern my_register_t r2;
extern my_register_t r3;
extern my_register_t r4;
extern my_register_t r5;
extern my_register_t r6;
extern my_register_t ret;

void push(enum Registers_e reg);
void pushd(int value);
void pop();
void add(enum Registers_e reg1, enum Registers_e reg2);
void add_direct(enum Registers_e reg1, int val);
void sub(enum Registers_e reg1, enum Registers_e reg2);
void sub_direct(enum Registers_e reg1, int val);
void mov(enum Registers_e reg1, enum Registers_e reg2);
void mov_direct(enum Registers_e reg1, int val);
void mul(enum Registers_e reg1, enum Registers_e reg2);
void mul_direct(enum Registers_e reg1, int val);
void cmp();
void print();
int opcode_dispatcher(char op);

#endif
