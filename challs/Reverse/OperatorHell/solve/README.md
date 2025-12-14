# Write-up OperatorHell

## Overview
- file: [OperatorHell](https://github.com/CyberNight-Efrei/CYBN-2025/blob/main/challs/Reverse/OperatorHell/dist/operator_hell)
- difficulty: hard
- Description: I hate maths and obvious code that much that i decided to change every of your operators. Try to relearn basic maths to validate my flag checker.

## Solution
This challenge is a little keygen which asks us to enter a key and then check it against a (nearly) constant value
tldr: antidebug + rc4 with a static iv.

### Init
Before we delve into the main there's an init function that you don't see by default because it's before the entry point. 

This strategy of hiding things in init has been seen a lot last years so i figured out i could add it just to add a bit more challenge.

* nullsub_2
```cpp
unsigned __int64 nullsub_2(void)
{
  int v0; // eax
  _BYTE v2[112]; // [rsp+0h] [rbp-A8h] BYREF
  _BYTE v3[40]; // [rsp+70h] [rbp-38h] BYREF
  unsigned __int64 v4; // [rsp+98h] [rbp-10h]

  v4 = __readfsqword(0x28u);
  v0 = SHA256_Init(v2);
  __asm { syscall; LINUX - }
  nullsub_0(v0 + 101);
  SHA256_Update(v2, "CYBN{a_little_bit_too_simple_and_not_even_leet}", 48LL);
  SHA256_Final(v3, v2);
  return v4 - __readfsqword(0x28u);
}
```
Reading this code doesn't give us a lot of information as we just see a sha256 done with a fake flag and thrown in the void.

But what's interesting there lies in the syscall and the call to nullsub_0.

Here if we take a look into the assembly we get :

```asm
.text:0000000000001180                 push    rbx
.text:0000000000001181                 sub     rsp, 0A0h
.text:0000000000001188                 mov     rdi, fs:28h
.text:0000000000001191                 mov     [rsp+0A8h+var_10], rdi
.text:0000000000001199                 mov     rdi, rsp
.text:000000000000119C                 call    _SHA256_Init
.text:00000000000011A1                 add     rax, 1
.text:00000000000011A5                 add     rax, 1
.text:00000000000011A9                 add     rax, 1
.text:00000000000011AD                 add     rax, 1
.text:00000000000011B1                 add     rax, 1
.text:00000000000011B5                 add     rax, 1
.text:00000000000011B9                 add     rax, 1
.text:00000000000011BD                 add     rax, 1
.text:00000000000011C1                 add     rax, 1
.text:00000000000011C5                 add     rax, 1
.text:00000000000011C9                 add     rax, 1
.text:00000000000011CD                 add     rax, 1
.text:00000000000011D1                 add     rax, 1
.text:00000000000011D5                 add     rax, 1
.text:00000000000011D9                 add     rax, 1
.text:00000000000011DD                 add     rax, 1
.text:00000000000011E1                 add     rax, 1
.text:00000000000011E5                 add     rax, 1
.text:00000000000011E9                 add     rax, 1
.text:00000000000011ED                 add     rax, 1
.text:00000000000011F1                 add     rax, 1
.text:00000000000011F5                 add     rax, 1
.text:00000000000011F9                 add     rax, 1
.text:00000000000011FD                 add     rax, 1
.text:0000000000001201                 add     rax, 1
.text:0000000000001205                 add     rax, 1
.text:0000000000001209                 add     rax, 1
.text:000000000000120D                 add     rax, 1
.text:0000000000001211                 add     rax, 1
.text:0000000000001215                 add     rax, 1
.text:0000000000001219                 add     rax, 1
.text:000000000000121D                 add     rax, 1
.text:0000000000001221                 add     rax, 1
.text:0000000000001225                 add     rax, 1
.text:0000000000001229                 add     rax, 1
.text:000000000000122D                 add     rax, 1
.text:0000000000001231                 add     rax, 1
.text:0000000000001235                 add     rax, 1
.text:0000000000001239                 add     rax, 1
.text:000000000000123D                 add     rax, 1
.text:0000000000001241                 add     rax, 1
.text:0000000000001245                 add     rax, 1
.text:0000000000001249                 add     rax, 1
.text:000000000000124D                 add     rax, 1
.text:0000000000001251                 add     rax, 1
.text:0000000000001255                 add     rax, 1
.text:0000000000001259                 add     rax, 1
.text:000000000000125D                 add     rax, 1
.text:0000000000001261                 add     rax, 1
.text:0000000000001265                 add     rax, 1
.text:0000000000001269                 add     rax, 1
.text:000000000000126D                 add     rax, 1
.text:0000000000001271                 add     rax, 1
.text:0000000000001275                 add     rax, 1
.text:0000000000001279                 add     rax, 1
.text:000000000000127D                 add     rax, 1
.text:0000000000001281                 add     rax, 1
.text:0000000000001285                 add     rax, 1
.text:0000000000001289                 add     rax, 1
.text:000000000000128D                 add     rax, 1
.text:0000000000001291                 add     rax, 1
.text:0000000000001295                 add     rax, 1
.text:0000000000001299                 add     rax, 1
.text:000000000000129D                 add     rax, 1
.text:00000000000012A1                 add     rax, 1
.text:00000000000012A5                 add     rax, 1
.text:00000000000012A9                 add     rax, 1
.text:00000000000012AD                 add     rax, 1
.text:00000000000012B1                 add     rax, 1
.text:00000000000012B5                 add     rax, 1
.text:00000000000012B9                 add     rax, 1
.text:00000000000012BD                 add     rax, 1
.text:00000000000012C1                 add     rax, 1
.text:00000000000012C5                 add     rax, 1
.text:00000000000012C9                 add     rax, 1
.text:00000000000012CD                 add     rax, 1
.text:00000000000012D1                 add     rax, 1
.text:00000000000012D5                 add     rax, 1
.text:00000000000012D9                 add     rax, 1
.text:00000000000012DD                 add     rax, 1
.text:00000000000012E1                 add     rax, 1
.text:00000000000012E5                 add     rax, 1
.text:00000000000012E9                 add     rax, 1
.text:00000000000012ED                 add     rax, 1
.text:00000000000012F1                 add     rax, 1
.text:00000000000012F5                 add     rax, 1
.text:00000000000012F9                 add     rax, 1
.text:00000000000012FD                 add     rax, 1
.text:0000000000001301                 add     rax, 1
.text:0000000000001305                 add     rax, 1
.text:0000000000001309                 add     rax, 1
.text:000000000000130D                 add     rax, 1
.text:0000000000001311                 add     rax, 1
.text:0000000000001315                 add     rax, 1
.text:0000000000001319                 add     rax, 1
.text:000000000000131D                 add     rax, 1
.text:0000000000001321                 add     rax, 1
.text:0000000000001325                 add     rax, 1
.text:0000000000001329                 add     rax, 1
.text:000000000000132D                 add     rax, 1
.text:0000000000001331                 add     rax, 1
.text:0000000000001335                 mov     rdi, 0
.text:000000000000133C                 mov     rsi, 0
.text:0000000000001343                 mov     rdx, 0
.text:000000000000134A                 mov     r10, 0
.text:0000000000001351                 syscall                 ; LINUX -
.text:0000000000001353                 mov     rdi, rax        ; int
.text:0000000000001356                 mov     rsi, 0
.text:000000000000135D                 mov     rdx, 0
.text:0000000000001364                 mov     r10, 0
.text:000000000000136B                 call    _Z9nullsub_0i   ; nullsub_0(int)
.text:0000000000001370                 lea     rsi, _ZL4cybn   ; "CYBN{a_little_bit_too_simple_and_not_ev"...
.text:0000000000001377                 mov     rdi, rsp
.text:000000000000137A                 mov     edx, 30h ; '0'
.text:000000000000137F                 call    _SHA256_Update
.text:0000000000001384                 lea     rdi, [rsp+0A8h+var_38]
.text:0000000000001389                 mov     rsi, rsp
.text:000000000000138C                 call    _SHA256_Final
.text:0000000000001391                 mov     rax, [rsp+0A8h+var_10]
.text:0000000000001399                 sub     rax, fs:28h
.text:00000000000013A2                 jnz     short loc_13AD
.text:00000000000013A4                 add     rsp, 0A0h
.text:00000000000013AB                 pop     rbx
.text:00000000000013AC                 retn
.text:00000000000013AD ;
```
Obviously the add rax, 1 are not generated by the compiler it's just a way to hide to ida the number of the syscall when coupled with the SHA256_INIT

We're doing this by using the fact that SHA256_init is supposed to return a 1 on success (here it should always succeed if not the challenge will break)

So we have 100 add rax,1 and the return value of SHA256_INIT which is 1 which will give us a ptrace PTRACE_ME call. the concept of this call is that it will fail and return -1 when there's already a debugger attached

then we call nullsub_0 with the result of the syscall. 

* nullsub_0
```cpp
const __m128i *__fastcall nullsub_0(unsigned int a1)
{
  const __m128i *result; // rax
  __m128i v2; // xmm1
  __m128i si128; // xmm0

  result = (const __m128i *)&iv;
  v2 = _mm_shuffle_epi32(_mm_cvtsi32_si128(a1), 0);
  do
  {
    si128 = _mm_load_si128(result++);
    result[-1] = _mm_add_epi32(si128, v2);
  }
  while ( (const __m128i *)((char *)&iv + 80) != result );
  return result;
}
```
Even though there's optimisations enabled with vector instruction, we can easily spot that it's just adding the argument to every elements of the iv thus making the iv false if you're debugging.

### Main
We can now delve into the real program

```cpp
int __fastcall main(int argc, const char **argv, const char **envp)
{
  int **v3; // rbp
  int *v4; // rax
  int *v5; // r13
  int *v6; // rax
  int *v7; // rax
  int *v8; // r12
  int *v9; // rax
  int *v10; // rbx
  _DWORD *v11; // rax
  __int64 v12; // rcx
  _DWORD *v13; // rax
  __int64 v14; // rcx
  _BYTE v16[32]; // [rsp+0h] [rbp-118h] BYREF
  _OWORD v17[9]; // [rsp+20h] [rbp-F8h] BYREF
  int v18; // [rsp+B0h] [rbp-68h]
  char s[40]; // [rsp+C0h] [rbp-58h] BYREF
  unsigned __int64 v20; // [rsp+E8h] [rbp-30h]

  v20 = __readfsqword(0x28u);
  v3 = (int **)operator new(0x20uLL);
  v4 = (int *)operator new(4uLL);
  *v4 = 0;
  v5 = v4;
  *v3 = v4;
  v6 = (int *)operator new(4uLL);
  *v6 = 0;
  v3[1] = v6;
  v7 = (int *)malloc(0x128uLL);
  v3[3] = v7;
  v8 = v7;
  v9 = (int *)malloc(0x800uLL);
  *v5 = 0;
  v3[2] = v9;
  v10 = v9;
  do
  {
    v11 = (_DWORD *)operator new(4uLL);
    v12 = *v5;
    *v11 = 0;
    *(_QWORD *)&v8[2 * v12] = v11;
    *v5 = v12 + 1;
  }
  while ( (int)v12 + 1 <= 36 );
  *v5 = 0;
  do
  {
    v13 = (_DWORD *)operator new(4uLL);
    v14 = *v5;
    *v13 = 0;
    *(_QWORD *)&v10[2 * v14] = v13;
    *v5 = v14 + 1;
  }
  while ( (int)v14 + 1 <= 255 );
  printf("Enter the string you wish to cipher :\n>> ");
  fgets(s, 37, _bss_start);
  v18 = 166;
  v17[0] = _mm_load_si128((const __m128i *)&xmmword_2110);
  v17[1] = _mm_load_si128((const __m128i *)&xmmword_2120);
  v17[2] = _mm_load_si128((const __m128i *)&xmmword_2130);
  v17[3] = _mm_load_si128((const __m128i *)&xmmword_2140);
  v17[4] = _mm_load_si128((const __m128i *)&xmmword_2150);
  v17[5] = _mm_load_si128((const __m128i *)&xmmword_2160);
  v17[6] = _mm_load_si128((const __m128i *)&xmmword_2170);
  v17[7] = _mm_load_si128((const __m128i *)&xmmword_2180);
  v17[8] = _mm_load_si128((const __m128i *)&xmmword_2190);
  OperatorShit::operator+(v16, v3, &iv);
  **v3 = 0;
  OperatorShit::operator-(v16, v3, s);
  if ( (unsigned int)OperatorShit::operator==(v3, v17) == 1 )
    puts("Sad");
  else
    puts("Cool");
  OperatorShit::operator*(v3, s);
  return 0;
}
```

This function is pretty big but in reality can be decomposed pretty well. 

First we have the part before the printf. We can easily spot that we are creating an object probably a struct or as it's cpp classes, in it we malloc two arrays respectively of size 0x128 (37 int elements) and 0x800 (256 int elements)

We fill those two arrays fully with another class we currently don't know anything about (and honestly we don't really care about it)

We then need ask for the string to cipher. This string must be a length of 37 (making the flag 37 length)
Then we load in v17 a 36 array of int (from xmm/vector data)
We can easily see that this v17 is compared with v3 in method OperatorShit::operator== and as it's not used before we know that our input will need to match v17 after being ciphered.

We then have two methods OperatorShit::operator+ and OperatorShit::operator- respectively using iv and our input. If we have a little bit of experience in cryptography we know that it's likely to be a symmetric cipher in two part. First the key scheduling and then the actual encryption.
You could just guess RC4 if you know me as i hate cryptography and i wouldn't go further than RC4 in cryptography. But to be sure about the guess we'll look at them.

### OperatorShit::operator+ (key scheduler)
```cpp
__m128i *__fastcall OperatorShit::operator+(__m128i *a1, int **a2, __int64 a3)
{
  __int64 *v6; // rax
  int *v7; // rsi
  __int64 v8; // rdi
  __int64 *v9; // r13
  __int64 v10; // rcx
  int v11; // eax
  __int64 v12; // rcx
  int *v13; // rdx
  _DWORD *v14; // rax
  __int64 v15; // r8
  __int64 v16; // rdi
  unsigned __int64 v17; // rdi
  int v18; // esi
  int *v19; // r9
  int *v20; // r10
  int v21; // eax
  int *v22; // rax
  int *v23; // rdx
  __int64 v24; // rcx
  __m128i *result; // rax

  v6 = (__int64 *)operator new(0x18uLL);
  v7 = *a2;
  v8 = 0LL;
  v6[2] = 0LL;
  v9 = v6;
  v10 = 0LL;
  *(_OWORD *)v6 = 0LL;
  v11 = 0;
  *v7 = 0;
  while ( 1 )
  {
    **(_DWORD **)&a2[2][2 * v11] = v11;
    v14 = (_DWORD *)(a3 + 4LL * (v11 % 20));
    if ( v10 == v8 )
    {
      std::vector<int>::_M_realloc_append<int const&>(v9, v14);
      v7 = *a2;
    }
    else
    {
      v12 = v10 + 4;
      *(_DWORD *)(v12 - 4) = *v14;
      v9[1] = v12;
    }
    v13 = v7;
    v11 = *v7 + 1;
    *v7 = v11;
    *a2 = v7;
    if ( v11 > 255 )
      break;
    v10 = v9[1];
    v8 = v9[2];
  }
  v15 = *v9;
  v16 = v9[1] - *v9;
  *a2[1] = 0;
  v17 = v16 >> 2;
  *v7 = 0;
  v18 = 0;
  do
  {
    if ( v18 >= v17 )
      OperatorShit::operator+(v17, v18, v13);
    v19 = a2[2];
    v20 = a2[1];
    v21 = (*(_DWORD *)(v15 + 4LL * v18) + **(_DWORD **)&v19[2 * v18] + *v20) % 256;
    *v20 = v21;
    v22 = &v19[2 * v21];
    v23 = &v19[2 * *v13];
    v24 = *(_QWORD *)v23;
    *(_QWORD *)v23 = *(_QWORD *)v22;
    *(_QWORD *)v22 = v24;
    v13 = *a2;
    v18 = **a2 + 1;
    *v13 = v18;
    *a2 = v13;
  }
  while ( v18 <= 255 );
  result = a1;
  *a1 = _mm_loadu_si128((const __m128i *)a2);
  a1[1] = _mm_loadu_si128((const __m128i *)a2 + 1);
  return result;
}
```
(You can easily know it's RC4 just by sending this to gpt and asking it for where this come from)
Else you can just see that we start by putting the whole iv in order in an array and then swapping it with at some point a modulo 256
Honestly here, just know by heart how RC4 functions and you'll see it directly.

### OperatorShit::operator- (encryption)
```cpp
__m128i *__fastcall OperatorShit::operator-(__m128i *a1, __m128i *a2, __int64 a3)
{
  int *v6; // rcx
  __int64 v7; // rdx
  int i; // eax
  int *v9; // rdi
  __int64 v10; // r11
  __int64 v11; // rsi
  int v12; // eax
  int v13; // eax
  __int64 *v14; // rax
  __int64 *v15; // rcx
  __int64 v16; // rdi
  _DWORD *v17; // rbx
  _DWORD *v18; // rbx
  __m128i *result; // rax

  v6 = (int *)a2->m128i_i64[0];
  v7 = a2[1].m128i_i64[0];
  for ( i = *(_DWORD *)a2->m128i_i64[0]; i <= 255; a2->m128i_i64[0] = (__int64)v6 )
  {
    **(_DWORD **)(v7 + 8LL * i) += *(char *)(a3 + i % 4);
    i = *v6 + 1;
    *v6 = i;
  }
  v9 = (int *)a2->m128i_i64[1];
  v10 = a2[1].m128i_i64[1];
  *v6 = 0;
  v11 = 0LL;
  *v9 = 0;
  do
  {
    v12 = (*v6 + 1) % 256;
    *v6 = v12;
    v13 = (**(_DWORD **)(v7 + 8LL * v12) + *v9) % 256;
    *v9 = v13;
    v14 = (__int64 *)(v7 + 8LL * v13);
    v15 = (__int64 *)(v7 + 8LL * *v6);
    v16 = *v15;
    *v15 = *v14;
    *v14 = v16;
    v6 = (int *)a2->m128i_i64[0];
    v9 = (int *)a2->m128i_i64[1];
    v17 = *(_DWORD **)(v7 + 8LL * *(int *)a2->m128i_i64[0]);
    LODWORD(v14) = **(_DWORD **)(v7 + 8LL * *v9) + *v17;
    *v17 = (_DWORD)v14;
    LODWORD(v14) = **(_DWORD **)(v7 + 8LL * ((int)v14 % 256)) ^ *(char *)(a3 + v11);
    v18 = *(_DWORD **)(v10 + 8 * v11++);
    *v18 = (_DWORD)v14;
  }
  while ( v11 != 37 );
  result = a1;
  *a1 = _mm_loadu_si128(a2);
  a1[1] = _mm_loadu_si128(a2 + 1);
  return result;
}
```
This one even worse just read about how RC4 works because i'll not explain it line by line.

### Solve
just take the original iv from the program and the flag to check against and throw it into any rc4 decryptor.
(Or just use chatgpt to instasolve the challenge because it became possible at the time of the cybn but not before)
CYBN{Wh0_5a1d_0p3r4t0rs_4r3_n0T_Fun}

## ending notes:
There should be a check somewhere about the flag starting with CYBN{ to not be able to try to decipher the rc4 with something which isn't starting with the right prefix
Unfortunately i wrote the challenge long ago and i forgot where it is.

