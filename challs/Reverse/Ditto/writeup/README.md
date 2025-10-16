# Solving (simple dybamic way)

1. Strace sur le ditto et constater la création d'un ELF

```
❯ strace ./ditto
...
futex(0xc000097158, FUTEX_WAKE_PRIVATE, 1) = 1
fcntl(1, F_GETFL)                       = 0x2 (flags O_RDWR)
fcntl(2, F_GETFL)                       = 0x2 (flags O_RDWR)
memfd_create("oom_reaper", 0)           = 4
write(4, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0`\22\0\0\0\0\0\0"..., 14480) = 14480
fork()                                  = 83731
exit_group(1)                           = ?
+++ exited with 1 +++
Unknown instructions.
```

2. Narrow down sur le syscall `write`

```
❯ strace -f -e trace=memfd_create,write -v -s 116000 ./ditto
strace: Process 89232 attached
strace: Process 89233 attached
strace: Process 89234 attached
strace: Process 89235 attached
strace: Process 89236 attached
[pid 89231] memfd_create("oom_reaper", 0) = 4
[pid 89231] write(4, "\177ELF\2\1\1\0\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0`\22\0\0\0\0\0\0@\0\0\0\0\0\0\0\2101\0\0\0\0\0\0\0\0\0\0@\08\0\16\0@\0\34\0\33\0\6\0\0\0\4\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0@\0\0\0\0\0\0\0\20\3\0\0\0\0\0\0\20\3\0\0\0\0\0\0\10\0\0\0\0\0\0\0\3\0\0\0\4\0\0\0\264\3\0\0\0\0\0\0\264\3\0\0\0\0\0\0\264\3\0\0\0\0\0\0\34\0\0\0\0\0\0\0\34\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\1\0\0\0\4\0\0\0\0\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\1\0\0\0\3\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0{0\0\0\0\0\0\0\6\1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0", 14480) = 14480
strace: Process 89239 attached
[pid 89232] ???( <unfinished ...>
```

3. Copier et sauvegarder le contenu du binaire 

```python
payload = b"\177ELF\2..."

with open("payload.bin", "wb") as f:
	f.write(payload)
```

4. Strings sur le payload

```
❯ l payload.bin && strings payload.bin 
.rw-r--r-- arch arch 14 KB Tue Oct 14 14:34:55 2025  payload.bin
\rnz6
/lib64/ld-linux-x86-64.so.2
puts
perror
__stack_chk_fail
__printf_chk
fread
fopen
strlen
strstr
__fprintf_chk
__libc_start_main
__cxa_finalize
fclose
libc.so.6
GLIBC_2.3.4
GLIBC_2.4
GLIBC_2.2.5
GLIBC_2.34
_ITM_deregisterTMCloneTable
__gmon_start__
_ITM_registerTMCloneTable
ATSH
[A\]
PTE1
u3UH
/tmp/instruction.txt
Unknown instructions.
give me the flag
/tmp/flag
Flag written to %s
Could not open flag file for writing
*0+'
6:<:
;*3$"
GCC: (GNU) 15.2.1 20250813
.shstrtab
.note.gnu.property
.note.gnu.build-id
.interp
.gnu.hash
.dynsym
.dynstr
.gnu.version
.gnu.version_r
.rela.dyn
.rela.plt
.init
.text
.fini
.rodata
.eh_frame_hdr
.eh_frame
.note.ABI-tag
.init_array
.fini_array
.dynamic
.got
.got.plt
.data
.bss
.comment
```

5. Constater le fichier `/tmp/instruction.txt` et l'instruction `give me the flag`, créer le fichier avec le bon contenu

```bash
echo "give me the flag" > /tmp/instruction.txt
```

6. Lancer une dernière fois le payload

```bash
chmod +x payload.bin 
./payload
cat /tmp/flag
```

7. Profit
