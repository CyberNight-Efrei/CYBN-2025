; reverse.asm
; NASM x86_64 Linux - key obfuscated with 0x45, flag stored XORed with repeating key
; Assemble: nasm -felf64 -o reverse_me.o reverse_me.asm
; Link:     ld -o reverse_me reverse_me.o
; Run:      ./reverse_me

section .data
    prompt      db  "Enter key: ", 0
    prompt_len  equ $-prompt

    ok_prefix   db  "yep, that key is good, here's your flag : ", 0
    ok_prefix_len equ $-ok_prefix

    nope_msg    db  "nope, wrong key", 10
    nope_len    equ $-nope_msg

    ; obfuscation constant for stored key bytes
    KEY_XOR_CONST equ 0x45

    ; expected key stored XORed by KEY_XOR_CONST (plain key: "Sup3rS3cr3tCYBN25k3y")
    expected_key_xored db 0x16,0x30,0x35,0x76,0x37,0x16,0x76,0x26,0x37,0x76
                       db 0x31,0x06,0x1C,0x07,0x0B,0x77,0x70,0x2E,0x76,0x3C
    expected_key_len   equ $-expected_key_xored

    ; flag stored XORed with the repeating plaintext key (plain flag: CYBN{N4SM_R3v3rs3_1s_N0t_D4t_H4rd})
    ; flag_len = 34
    flag_xored db 0x10,0x2C,0x32,0x7D,0x09,0x1D,0x07,0x30,0x3F,0x6C
              db 0x26,0x70,0x2F,0x71,0x3C,0x41,0x06,0x34,0x02,0x0A
              db 0x0C,0x3B,0x40,0x47,0x2D,0x17,0x07,0x17,0x2D,0x7B
              db 0x40,0x31,0x3D,0x3F
    flag_len equ 34

    newline_w db 10

section .bss
    key_buf    resb 64                    ; read input
    key_plain  resb expected_key_len      ; decoded key will live here temporarily
    decoded    resb flag_len + 1          ; decoded flag + null

section .text
    global _start

_start:
    ; print prompt
    mov     rax, 1
    mov     rdi, 1
    mov     rsi, prompt
    mov     rdx, prompt_len
    syscall

    ; read key from stdin
    mov     rax, 0
    mov     rdi, 0
    mov     rsi, key_buf
    mov     rdx, 64
    syscall
    cmp     rax, 1
    jb      .wrong_key        ; nothing read or error (or zero-length)

    mov     rbx, rax          ; bytes read (including newline)
    mov     rcx, rbx          ; rcx = working length

    ; strip trailing newline(s) (while rcx > 0 and last byte is 0x0A/0x0D, rcx--)
.strip_nl:
    cmp     rcx, 0
    je      .after_strip
    mov     rax, rcx
    dec     rax               ; index = rcx - 1
    mov     al, [key_buf + rax]
    cmp     al, 0x0A
    je      .dec_len
    cmp     al, 0x0D
    je      .dec_len
    jmp     .after_strip
.dec_len:
    dec     rcx
    jmp     .strip_nl

.after_strip:
    ; rcx now = key_len (without newline)
    cmp     rcx, expected_key_len
    jne     .wrong_key

    ; decode expected_key_xored -> key_plain by xor with KEY_XOR_CONST
    xor     rsi, rsi            ; i = 0
.decode_key:
    mov     al, [rel expected_key_xored + rsi]
    xor     al, KEY_XOR_CONST
    mov     [key_plain + rsi], al
    inc     rsi
    cmp     rsi, expected_key_len
    jb      .decode_key

    ; compare user input (key_buf[0..rcx-1]) with key_plain
    xor     rdi, rdi
.compare_loop:
    mov     al, [key_buf + rdi]
    mov     bl, [key_plain + rdi]
    cmp     al, bl
    jne     .wipe_and_wrong
    inc     rdi
    cmp     rdi, expected_key_len
    jb      .compare_loop

    ; key matches -> decode flag: flag_xored XOR key_plain (repeating)
    xor     rsi, rsi        ; flag index
    xor     r8, r8          ; key index
.decode_flag:
    mov     al, [rel flag_xored + rsi]
    mov     bl, [key_plain + r8]
    xor     al, bl
    mov     [decoded + rsi], al

    inc     rsi
    inc     r8
    mov     rax, expected_key_len
    cmp     r8, rax
    jb      .no_wrap
    xor     r8, r8
.no_wrap:
    cmp     rsi, flag_len
    jb      .decode_flag

    ; null terminate decoded
    mov     byte [decoded + flag_len], 0

    ; print ok prefix
    mov     rax, 1
    mov     rdi, 1
    mov     rsi, ok_prefix
    mov     rdx, ok_prefix_len
    syscall

    ; print decoded flag
    mov     rax, 1
    mov     rdi, 1
    mov     rsi, decoded
    mov     rdx, flag_len
    syscall

    ; print newline
    mov     rax, 1
    mov     rdi, 1
    mov     rsi, newline_w
    mov     rdx, 1
    syscall

    ; wipe sensitive buffers: key_plain, key_buf (only up to original read length), decoded
.wipe_and_exit:
    xor     rsi, rsi
.wipe_key_plain:
    mov     byte [key_plain + rsi], 0
    inc     rsi
    cmp     rsi, expected_key_len
    jb      .wipe_key_plain

    ; wipe key_buf using original read length in rbx
    mov     rdx, rbx
    xor     rsi, rsi
.wipe_key_buf:
    mov     byte [key_buf + rsi], 0
    inc     rsi
    cmp     rsi, rdx
    jb      .wipe_key_buf

    ; wipe decoded (flag_len)
    xor     rsi, rsi
.wipe_decoded:
    mov     byte [decoded + rsi], 0
    inc     rsi
    cmp     rsi, flag_len
    jb      .wipe_decoded

    ; exit 0
    mov     rax, 60
    xor     rdi, rdi
    syscall

.wipe_and_wrong:
    ; wipe buffers then print wrong message
    jmp     .wipe_and_exit

.wrong_key:
    mov     rax, 1
    mov     rdi, 1
    mov     rsi, nope_msg
    mov     rdx, nope_len
    syscall
    jmp     .wipe_and_exit
