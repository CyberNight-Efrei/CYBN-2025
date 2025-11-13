default_target=all
.PHONY: default_target

all: code real

code:
	gcc -fstack-protector-strong -fno-pie -no-pie -Wl,-z,relro,-z,now -o main src/main.c

real:
	cp flag.txt /flag
