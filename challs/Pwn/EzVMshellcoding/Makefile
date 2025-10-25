default_target=all
.PHONY: default_target

all: code real

code:
	gcc -s src/main.c src/opcode.c src/syscall.c -o vm -m32

real:
	cp flag.txt /flag
