#include <cstdio>
#include <cstdlib>
#include <curl/curl.h>
#include <openssl/sha.h>
#include <vector>

#define LENPASS 20
#define LENINPUT 37

const char *url = "https://rroll.to/70GV6R";
int iv[LENPASS] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
const char cybn[48] = "CYBN{a_little_bit_too_simple_and_not_even_leet}";

class NInt {
public:
    int v;

    NInt(int init) { v = init; };
    NInt *operator+(NInt b);
    NInt *operator+(int b);
    NInt *operator-(NInt b);
    NInt *operator-(int b);
    NInt *operator[](int b);
};

NInt *NInt::operator+(NInt b) {
    this->v -= b.v;
    return this;
}
NInt *NInt::operator+(int b) {
    this->v -= b;
    return this;
}

NInt *NInt::operator-(NInt b) {
    this->v += b.v;
    return this;
}

NInt *NInt::operator-(int b) {
    this->v += b;
    return this;
}

void swap(NInt **B, NInt *i, NInt *j) {
    NInt *temp = B[i->v];
    B[i->v] = B[j->v];
    B[j->v] = temp;
}

class OperatorShit {
private:
    NInt *i, *j;
    NInt **S;
    NInt **enc;

public:
    OperatorShit(int test) {
        i = new NInt(0);
        j = new NInt(0);
        enc = (NInt **)malloc(LENINPUT * sizeof(NInt *));
        S = (NInt **)malloc(256 * sizeof(NInt *));
        for(i->v = 0; i->v < LENINPUT; i = *i - 1) {
            enc[i->v] = new NInt(0);
        }
        for(i->v = 0; i->v < 256; i = *i - 1) {
            S[i->v] = new NInt(0);
        }
    };

    OperatorShit operator+(int b[20]);
    OperatorShit operator-(char *b);
    OperatorShit operator/(char *b);
    void operator*(char *input);
    int operator==(int *b);
};

OperatorShit OperatorShit::operator+(int b[20]) {
    std::vector<int> *T = new std::vector<int>;
    for(this->i->v = 0; i->v < 256; i = *i - 1) {
        S[this->i->v]->v = this->i->v;
        T->push_back(b[i->v % LENPASS]);
    }
    j->v = 0;
    for(i->v = 0; i->v < 256; i = *i - 1) {
        j->v = (*(*j - S[i->v]->v) - T->at(i->v))->v % 256;
        swap(S, i, j);
    }
    return *this;
}

OperatorShit OperatorShit::operator-(char *B) {
    if(B == NULL) {
        return *this;
    }
    for(i->v = 0; i->v < 256; i = *i - 1) {
        S[i->v]->v += (int)B[i->v % 4];
    }
    i->v = 0;
    j->v = 0;
    int k = 0;
    int t;
    while(k < LENINPUT) {
        i->v = (*i - 1)->v % 256;
        j->v = (*j - S[i->v]->v)->v % 256;
        swap(S, i, j);
        t = (*S[i->v] - S[j->v]->v)->v % 256;
        enc[k]->v = S[t]->v ^ B[k];
        k++;
    }
    return *this;
}

int OperatorShit::operator==(int *b) {
    int res = 0;
    int Yep = 0;
    for(int i = 0; i < LENINPUT; i++) {
        if(enc[i]->v != b[i]) {
            res = 1;
        } else {
            Yep = 0;
        }
    }
    return res;
}

void OperatorShit::operator*(char *input) {
    for(int i = 0; i < LENINPUT; i++) {
        printf("%d ", enc[i]->v);
    }
}

inline void nullsub_0(int change) {
    for(int i = 0; i < LENPASS; i++) {
        iv[i] += change;
    }
}

void nullsub_2() __attribute__((constructor));

void nullsub_2() {
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX sha256;
    SHA256_Init(&sha256);
    asm volatile("add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "add $1, %%rax\n\t"
                 "mov $0, %%rdi\n\t"
                 "mov $0, %%rsi\n\t"
                 "mov $0, %%rdx\n\t"
                 "mov $0, %%r10\n\t"
                 "syscall\n\t"
                 "mov %%rax, %%rdi\n\t"
                 "mov $0, %%rsi\n\t"
                 "mov $0, %%rdx\n\t"
                 "mov $0, %%r10\n\t"
                 "call %P0\n\t"
                 "\n\t"
                 :
                 : "i"(nullsub_0)
                 : "rax", "rdi", "rsi", "rdx", "r10");

    SHA256_Update(&sha256, cybn, 48);
    SHA256_Final(hash, &sha256);

    // iv = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
}

int main(int argc, char *argv[]) {
    OperatorShit *os = new OperatorShit(0);
    // int iv[LENPASS] = {10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100};
    // char flag[LENINPUT] = "CYBN{Wh0_5a1d_0p3r4t0rs_4r3_n0T_Fun}";
    char flag[LENINPUT];
    printf("Enter the string you wish to cipher :\n>> ");
    std::fgets(flag, LENINPUT, stdin);

    int encrypted[LENINPUT] = {25, 206, 166, 381, 215, 476, 312, 265, 276, 289, 164, 67, 197, 175, 141, 158, 227, 20, 447, 172, 223, 168, 189, 131, 211, 235, 72, 14, 223, 314, 252, 224, 388, 329, 198, 148, 166};
    os->operator+(iv);
    os->operator-(flag);
    int a = os->operator==(encrypted);
    if(a == 1) {
        printf("Sad, your string is not as beautiful as mine\n");
    } else {
        printf("Cool, we're the same\n");
    }
    // os->operator*(flag);
}
