# Write-up EzVMShellcoding

## Overview
- Number of solve : 0
- file : [vm](https://github.com/CyberNight-Efrei/CYBN-2025/blob/main/challs/Pwn/EzVMshellcoding/dist/vm)
- Difficulty : Medium
- Description : I made this new vm because i didn't like having to use non printable chars.
  Could you try to escape from it to get the flag in /flag for me

## Solution
This challenge is a custom VM which executes an unknown set of instruction. From the description, every instruction should be printable characters and thus ascii.

We thus need to start by reverse engineering the VM.


### Main

```C
int sub_12D7()
{
  int v0; // eax
  int i; // [esp+2h] [ebp-Ch]

  sub_1268();
  for ( i = 0; !i; i = sub_1C18(byte_50A0[v0]) )
    v0 = dword_5038++;
  if ( i == -1 )
    printf("NOPE you aren't allowed this (but i won't tell you what)");
  return 0;
}
```
After a quick renaming we have :
```C
int __cdecl main(int argc, const char **argv, const char **envp)
{
  int v3; // eax
  int i; // [esp+2h] [ebp-Ch]

  getinput();
  for ( i = 0; !i; i = dispatcher(input[v3]) )
    v3 = reg_ip++;
  if ( i == -1 )
    printf("NOPE you aren't allowed this (but i won't tell you what)");
  return 0;
}
```

### Dispatcher
```C
int __cdecl dispatcher(char a1)
{
  int v1; // edx
  int v2; // edx
  int v3; // edx
  int v4; // edx
  int v6; // edx
  int v7; // edx
  int v8; // edx
  int v9; // edx
  int v10; // edx
  int v11; // edx
  int v12; // edx
  int v13; // edx
  int v14; // edx
  int v15; // edx
  int v16; // edx
  int v17; // edx
  int v18; // edx
  int v19; // edx
  int v20; // edx
  int v21; // [esp+10h] [ebp-18h]
  int v22; // [esp+14h] [ebp-14h]
  int v23; // [esp+14h] [ebp-14h]
  int v24; // [esp+14h] [ebp-14h]
  int v25; // [esp+14h] [ebp-14h]
  int v26; // [esp+14h] [ebp-14h]
  int v27; // [esp+14h] [ebp-14h]
  int v28; // [esp+14h] [ebp-14h]
  int v29; // [esp+14h] [ebp-14h]
  int v30; // [esp+18h] [ebp-10h]
  int v31; // [esp+18h] [ebp-10h]
  int v32; // [esp+18h] [ebp-10h]
  int v33; // [esp+18h] [ebp-10h]
  int v34; // [esp+18h] [ebp-10h]

  v21 = 0;
  if ( a1 == 85 )
    return 1;
  if ( a1 > 85 )
    return 2;
  if ( a1 == 84 )
  {
    v20 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v20 + 1);
    sub_22D8(input[v20]);
    return v21;
  }
  if ( a1 > 84 )
    return 2;
  if ( a1 == 83 )
  {
    sub_1BDB();
    return v21;
  }
  if ( a1 > 83 )
    return 2;
  if ( a1 == 82 )
  {
    sub_1BA8();
    return v21;
  }
  if ( a1 > 82 )
    return 2;
  if ( a1 == 81 )
  {
    v18 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v18 + 1);
    v29 = input[v18];
    v19 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v19 + 1);
    v34 = input[v19];
    if ( v34 <= 31 )
      return -1;
    sub_19EE(v29, v34);
    return v21;
  }
  if ( a1 > 81 )
    return 2;
  if ( a1 == 80 )
  {
    v16 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v16 + 1);
    v28 = input[v16];
    v17 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v17 + 1);
    sub_1B79(v28, input[v17]);
    return v21;
  }
  if ( a1 > 80 )
    return 2;
  if ( a1 == 73 )
  {
    v3 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v3 + 1);
    v23 = input[v3];
    v4 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v4 + 1);
    v30 = input[v4];
    if ( v30 <= 31 )
      return -1;
    sub_18A6(v23, v30);
    return v21;
  }
  if ( a1 > 73 )
    return 2;
  if ( a1 == 72 )
  {
    v1 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v1 + 1);
    v22 = input[v1];
    v2 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v2 + 1);
    sub_19BF(v22, input[v2]);
    return v21;
  }
  if ( a1 > 72 )
    return 2;
  if ( a1 == 71 )
  {
    v14 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v14 + 1);
    v27 = input[v14];
    v15 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v15 + 1);
    v33 = input[v15];
    if ( v33 <= 31 )
      return -1;
    sub_16F5(v27, v33);
    return v21;
  }
  if ( a1 > 71 )
    return 2;
  if ( a1 == 70 )
  {
    v12 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v12 + 1);
    v26 = input[v12];
    v13 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v13 + 1);
    sub_1877(v26, input[v13]);
    return v21;
  }
  if ( a1 > 70 )
    return 2;
  if ( a1 == 69 )
  {
    v10 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v10 + 1);
    v25 = input[v10];
    v11 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v11 + 1);
    v32 = input[v11];
    if ( v32 <= 31 )
      return -1;
    sub_1532(v25, v32);
    return v21;
  }
  if ( a1 > 69 )
    return 2;
  if ( a1 == 68 )
  {
    v8 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v8 + 1);
    v24 = input[v8];
    v9 = (int)*(&off_5034 + 1);
    *(&off_5034 + 1) = (_UNKNOWN *)(v9 + 1);
    sub_16C6(v24, input[v9]);
    return v21;
  }
  if ( a1 > 68 )
    return 2;
  if ( a1 == 67 )
  {
    sub_14EE();
    return v21;
  }
  if ( a1 > 67 )
    return 2;
  if ( a1 != 65 )
  {
    if ( a1 == 66 )
    {
      v7 = (int)*(&off_5034 + 1);
      *(&off_5034 + 1) = (_UNKNOWN *)(v7 + 1);
      v31 = input[v7];
      if ( v31 <= 31 )
        return -1;
      sub_1481(v31);
      return v21;
    }
    return 2;
  }
  v6 = (int)*(&off_5034 + 1);
  *(&off_5034 + 1) = (_UNKNOWN *)(v6 + 1);
  sub_14B6(input[v6]);
  return v21;
}
```

The dispatcher code can be daunting at first but in reality some things have been done to make it easy to reverse

#### Register
First we can spot a lot of variable with offset + 1, clearly a variable in a struct then probably something interesting.

Checking off_503C
```aiignore
.data:0000503C off_503C        dd offset unk_300E  // contains r1
.data:00005040                 dd 0
```
Seeing this we understand that this is a register struct with the name of the register to help us

We can define the struct s_reg and apply it to all registers
```C
00000000 struct s_reg // sizeof=0x8
00000000     char *s_reg;
00000004     int value;
00000008 };
```
!! Doing This will break the naming of reg_ip in the main function but we don't really care about it because we already know what it's doing

Then after the renaming of all those struct we have all the registers correctly defined and you could probably send it to gpt to let it solve.

#### OPCODES
If you enter any character which is not an opcode, you'll just get out of the loop and the program won't read the end of your input
We'll reverse the opcodes one by one :

---
##### opcode 'U'
```C
 if ( opcode == 'U' )
    return 1;
```
Just a natural exit opcode

---
##### opcode 'T'
```C
 if ( opcode == 'T' )
  {
    v20 = reg_ip.value;
    reg_ip.value = v20 + 1;
    sub_22D8(input[v20]);
    return v21;
  }
```
```C
int __cdecl sub_22D8(char a1)
{
  int result; // eax

  result = a1;
  if ( a1 == 66 )
    return fopen_modified();
  if ( a1 == 67 )
    return fread_modified();
  return result;
}
```
```C
char *fopen_modified()
{
  char *result; // eax
  FILE *v1; // edx
  char *haystack; // [esp+8h] [ebp-10h]

  result = (char *)reg_ret.value;
  if ( !result )
  {
    haystack = &byte_5120[reg_r1.value];
    if ( strstr(haystack, "/etc")
      || strstr(haystack, "/proc")
      || strstr(haystack, "/dev")
      || strstr(haystack, "/tmp")
      || strstr(haystack, "/home")
      || (result = strstr(haystack, "/mnt")) != 0 )
    {
      v1 = fopen(haystack, &byte_5120[reg_r2.value]);
      result = (char *)&reg_ret;
      reg_ret.value = (int)v1;
    }
  }
  return result;
}
```
```C
Elf32_Dyn **fread_modified()
{
  Elf32_Dyn **result; // eax

  result = &off_4FF4;
  if ( !reg_ret.value && reg_r2.value >= reg_r3.value )
    return (Elf32_Dyn **)fread(&byte_5120[reg_r2.value], 1u, reg_r3.value, (FILE *)reg_r1.value);
  return result;
}
```
We can easily understand looking at these two last functions that opcode T is a syscall.

From the second function we see that we either go in the fopen_modified or fread_modified function whether the character next to ip is a B or a C

###### fopen

From the decompilation of the function we notice that we read the filepath from our stack which is byte_5120 at index of the value of register r1

We also notice that we are not allowed to open directly /flag as we check that the file we're opening has in it's filepath:
- /etc
- /proc
- /dev
- /tmp
- /home
- /mnt

This check is easy to bypass by knowing that every process has access to it's root directory from /proc/self/root

Finally the pointer of the FILE is put in the return register

###### fread

The fread function check that the ret register is equal to 0 and that the index in the stack where it will read the content of the file is greater than the size of what we try to read

so to read a file we need to have:
- index to store content in r2
- size to read in r3
- file pointer in r1

--- 
##### Opcode 'S'

```C
if ( opcode == 'S' )
  {
    sub_1BDB();
    return v21;
  }
```
```C
int sub_1BDB()
{
  return printf("%s", &byte_5120[reg_sp.value]);
}
```

This opcode is just the way of printing the string at the current stack pointer

---
##### Opcode 'R'

```C
 if ( opcode == 'R' )
  {
    sub_1BA8();
    return v21;
  }
```
```C
s_reg *sub_1BA8()
{
  s_reg *result; // eax

  result = &reg_ret;
  reg_ret.value = reg_r1.value == reg_r2.value;
  return result;
}
```
This Opcode is a cmp between r1 and r2 and it returns the result in ret

This opcode is used simply as
R

---
##### Opcode 'Q'

```C
 if ( opcode == 'Q' )
  {
    v18 = reg_ip.value;
    reg_ip.value = v18 + 1;
    v29 = input[v18];
    v19 = reg_ip.value;
    reg_ip.value = v19 + 1;
    v34 = input[v19];
    if ( v34 <= 31 )
      return -1;
    sub_19EE(v29, v34);
    return v21;
  }
```
```C
s_reg *__cdecl sub_19EE(unsigned int a1, int a2)
{
  s_reg *result; // eax

  result = (s_reg *)&off_4FF4;
  if ( a1 == 80 )
  {
    result = &reg_ret;
    reg_ret.value *= a2;
  }
  else if ( a1 <= 0x50 )
  {
    if ( a1 == 73 )
    {
      result = &reg_r6;
      reg_r6.value *= a2;
    }
    else if ( a1 <= 0x49 )
    {
      switch ( a1 )
      {
        case 'H':
          result = &reg_r5;
          reg_r5.value *= a2;
          break;
        case 'G':
          result = &reg_r4;
          reg_r4.value *= a2;
          break;
        case 'F':
          result = &reg_r3;
          reg_r3.value *= a2;
          break;
        case 'E':
          result = &reg_r2;
          reg_r2.value *= a2;
          break;
        case 'D':
          result = &reg_r1;
          reg_r1.value *= a2;
          break;
        case 'B':
          result = &reg_sp;
          reg_sp.value *= a2;
          break;
        case 'C':
          result = &reg_ip;
          reg_ip.value *= a2;
          break;
      }
    }
  }
  return result;
}
```
This opcode is clearly a mul opcode. it multiplies the content of a register in place by an immediate value

This opcode is used as:   
'Q' | reg_to_multiply | multiplying_value

---
##### Opcode 'P'

```C
 if ( opcode == 'P' )
  {
    v16 = reg_ip.value;
    reg_ip.value = v16 + 1;
    v28 = input[v16];
    v17 = reg_ip.value;
    reg_ip.value = v17 + 1;
    sub_1B79(v28, input[v17]);
    return v21;
  }
```
```C
s_reg *__cdecl sub_1B79(unsigned int a1, int a2)
{
  int v3; // [esp+Ch] [ebp-4h]

  v3 = get_reg_value(a2);
  return sub_19EE(a1, v3);
}
```
This opcode is also a mul but it's a mul using reg instead of immediate value

This opcode is used as:    
'P' | reg_to_multiply | reg_to_multiply_with

---
##### Opcode 'I'

```C
 if ( opcode == 'I' )
  {
    v3 = reg_ip.value;
    reg_ip.value = v3 + 1;
    v23 = input[v3];
    v4 = reg_ip.value;
    reg_ip.value = v4 + 1;
    v30 = input[v4];
    if ( v30 <= 31 )
      return -1;
    sub_18A6(v23, v30);
    return v21;
  }
```
```C
s_reg *__cdecl sub_18A6(unsigned int a1, int a2)
{
  s_reg *result; // eax

  result = (s_reg *)&off_4FF4;
  if ( a1 == 80 )
  {
    result = &reg_ret;
    reg_ret.value = a2;
  }
  else if ( a1 <= 0x50 )
  {
    if ( a1 == 73 )
    {
      result = &reg_r6;
      reg_r6.value = a2;
    }
    else if ( a1 <= 0x49 )
    {
      switch ( a1 )
      {
        case 'H':
          result = &reg_r5;
          reg_r5.value = a2;
          break;
        case 'G':
          result = &reg_r4;
          reg_r4.value = a2;
          break;
        case 'F':
          result = &reg_r3;
          reg_r3.value = a2;
          break;
        case 'E':
          result = &reg_r2;
          reg_r2.value = a2;
          break;
        case 'D':
          result = &reg_r1;
          reg_r1.value = a2;
          break;
        case 'B':
          result = &reg_sp;
          reg_sp.value = a2;
          break;
        case 'C':
          result = &reg_ip;
          reg_ip.value = a2;
          break;
      }
    }
  }
  return result;
}
```
This opcode is a mov immediate one

This opcode is used as:    
'I' | reg_dst | immediate value

---
##### Opcode 'H'

```C
if ( opcode == 'H' )
  {
    v1 = reg_ip.value;
    reg_ip.value = v1 + 1;
    v22 = input[v1];
    v2 = reg_ip.value;
    reg_ip.value = v2 + 1;
    sub_19BF(v22, input[v2]);
    return v21;
  }
```
```C
s_reg *__cdecl sub_19BF(unsigned int a1, unsigned int a2)
{
  int reg_value; // [esp+Ch] [ebp-4h]

  reg_value = get_reg_value(a2);
  return sub_18A6(a1, reg_value);
}
```
This opcode is also a mov but from register to register

This opcode is used as:    
'H' | reg_dst | reg_src

---
##### Opcode 'G'

```C
 if ( opcode == 'G' )
  {
    v14 = reg_ip.value;
    reg_ip.value = v14 + 1;
    v27 = input[v14];
    v15 = reg_ip.value;
    reg_ip.value = v15 + 1;
    v33 = input[v15];
    if ( v33 <= 31 )
      return -1;
    sub_16F5(v27, v33);
    return v21;
  }
```
```C
s_reg *__cdecl sub_16F5(unsigned int a1, int a2)
{
  s_reg *result; // eax

  result = (s_reg *)&off_4FF4;
  if ( a1 == 80 )
  {
    result = &reg_ret;
    reg_ret.value -= a2;
  }
  else if ( a1 <= 0x50 )
  {
    if ( a1 == 73 )
    {
      result = &reg_r6;
      reg_r6.value -= a2;
    }
    else if ( a1 <= 0x49 )
    {
      switch ( a1 )
      {
        case 'H':
          result = &reg_r5;
          reg_r5.value -= a2;
          break;
        case 'G':
          result = &reg_r4;
          reg_r4.value -= a2;
          break;
        case 'F':
          result = &reg_r3;
          reg_r3.value -= a2;
          break;
        case 'E':
          result = &reg_r2;
          reg_r2.value -= a2;
          break;
        case 'D':
          result = &reg_r1;
          reg_r1.value -= a2;
          break;
        case 'B':
          result = &reg_sp;
          reg_sp.value -= a2;
          break;
        case 'C':
          result = &reg_ip;
          reg_ip.value -= a2;
          break;
      }
    }
  }
  return result;
}
```
This is a immediate sub opcode

This opcode is used as:   
'G' | reg_dst | immediate value

---
##### Opcode 'F'

```C
 if ( opcode == 'F' )
  {
    v12 = reg_ip.value;
    reg_ip.value = v12 + 1;
    v26 = input[v12];
    v13 = reg_ip.value;
    reg_ip.value = v13 + 1;
    sub_1877(v26, input[v13]);
    return v21;
  }
```
```C
s_reg *__cdecl sub_1877(unsigned int a1, unsigned int a2)
{
  int reg_value; // [esp+Ch] [ebp-4h]

  reg_value = get_reg_value(a2);
  return sub_16F5(a1, reg_value);
}
```
This opcode is a sub from register to register

This opcode is used as:    
'F' | reg_dst | reg_src

---
##### Opcode 'E'

```C
if ( opcode == 'E' )
  {
    v10 = reg_ip.value;
    reg_ip.value = v10 + 1;
    v25 = input[v10];
    v11 = reg_ip.value;
    reg_ip.value = v11 + 1;
    v32 = input[v11];
    if ( v32 <= 31 )
      return -1;
    sub_1532(v25, v32);
    return v21;
  }
```
```C
s_reg *__cdecl sub_1532(unsigned int a1, int a2)
{
  s_reg *result; // eax

  result = (s_reg *)&off_4FF4;
  if ( a1 == 80 )
  {
    result = &reg_ret;
    reg_ret.value += a2;
  }
  else if ( a1 <= 0x50 )
  {
    if ( a1 == 73 )
    {
      result = &reg_r6;
      reg_r6.value += a2;
    }
    else if ( a1 <= 0x49 )
    {
      switch ( a1 )
      {
        case 'H':
          result = &reg_r5;
          reg_r5.value += a2;
          break;
        case 'G':
          result = &reg_r4;
          reg_r4.value += a2;
          break;
        case 'F':
          result = &reg_r3;
          reg_r3.value += a2;
          break;
        case 'E':
          result = &reg_r2;
          reg_r2.value += a2;
          break;
        case 'D':
          result = &reg_r1;
          reg_r1.value += a2;
          break;
        case 'B':
          result = &reg_sp;
          reg_sp.value += a2;
          break;
        case 'C':
          result = &reg_ip;
          reg_ip.value += a2;
          break;
      }
    }
  }
  return result;
}
```
This opcode is an immediate add

This opcode is used as:    
'E' | reg_dst | immediate value

---
##### Opcode 'D'

```C
 if ( opcode == 'D' )
  {
    v8 = reg_ip.value;
    reg_ip.value = v8 + 1;
    v24 = input[v8];
    v9 = reg_ip.value;
    reg_ip.value = v9 + 1;
    sub_16C6(v24, input[v9]);
    return v21;
  }
```
```C
s_reg *__cdecl sub_16C6(unsigned int a1, unsigned int a2)
{
  int reg_value; // [esp+Ch] [ebp-4h]

  reg_value = get_reg_value(a2);
  return sub_1532(a1, reg_value);
}
```
This opcode is a register to register add

This opcode is used as:    
'D' | reg_dst | reg_src

---
##### Opcode 'C'

```C
if ( opcode == 'C' )
{
    sub_14EE();
    return v21;
}
```
```C
s_reg *sub_14EE()
{
  s_reg *result; // eax

  --reg_sp.value;
  result = &reg_ret;
  reg_ret.value = byte_5120[reg_sp.value];
  return result;
}
```
This opcode is a pop instruction. 

This opcode is used as:    
'C'

---
##### Opcode 'B'

```C
if ( opcode == 66 )
{
      v7 = reg_ip.value;
      reg_ip.value = v7 + 1;
      v31 = input[v7];
      if ( v31 <= 31 )
        return -1;
      sub_1481(v31);
      return v21;
}
```
```C
char *__cdecl sub_1481(char a1)
{
  int value; // edx
  char *result; // eax

  value = reg_sp.value;
  reg_sp.value = value + 1;
  result = byte_5120;
  byte_5120[value] = a1;
  return result;
}
```
This opcode is a push immediate instruction

This opcode is used as:     
'B' | immediate value

---
##### Opcode 'A'
```C
  v6 = reg_ip.value;
  reg_ip.value = v6 + 1;
  sub_14B6(input[v6]);
  return v21;
```
```C
char *__cdecl sub_14B6(unsigned int a1)
{
  char *result; // eax
  char reg_value; // [esp+Ch] [ebp-4h]

  result = (char *)&off_4FF4;
  if ( a1 != 'C' && a1 != 'B' )
  {
    reg_value = get_reg_value(a1);
    return sub_1481(reg_value);
  }
  return result;
}
```
This opcode is a push instruction from register to register.
It cannot push sp and ip registers

This opcode is used as 
'A' | reg_src

### Shellcoding

At this point, all the reversing is done.    

we have every instruction that we need. We can just make a little read shellcode    

To do this we know that we'll need the filepath in the stack   
so we need to push "/proc/self/root/flag"
then we need to push 'r' for the fopen

we also need to make the register get the good value

We'll then make our shellcode this way:

**B/BpBrBoBcB/BsBeBlBfB/BrBoBoBtB/BfBlBaBg** # push '/proc/self/root/flag'    
**EB0** # add 48 (ord("0")) to reg sp    
**Br** # push 'r'   
**IED** # mov 68 (ord("D")) in reg r2   
**TB** # syscall fopen : r1 is still at 0 and our path is at the bottom of the stack so 0, r2 is at len("/proc/self/root/flag") + 32 = 68   
**HDP** # mov return register into r1 register | file pointer   
**HBE** # mov r2 register into sp | index to store the read   
**IF!** # mov 33 (ord("!")) in reg r3 | size of the read   
**IP0** # mov 48 (ord("0")) in return register   
**GP0** # substract 48 (ord("0")) from return register | we make the ret register equal to 0  
**TC** # syscall fread   
**S** # as r2 is equal to sp, we read the file at the index sp in the stack, we can just print it  

Final shellcode :
B/BpBrBoBcB/BsBeBlBfB/BrBoBoBtB/BfBlBaBgEB0BrIEDTBHDPHBEIF!IP0GP0TCS
