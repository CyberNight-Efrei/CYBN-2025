#include <stdio.h>
#include <math.h>
#include <string.h>

double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

const double weights_hidden[32][4] = {
    {0.34, -0.92, 0.77, -0.61}, {0.51, 0.18, -0.39, 0.28}, {-0.62, 0.49, 0.55, 0.12},
    {0.44, 0.65, -0.21, -0.56}, {-0.35, -0.77, 0.69, -0.14}, {0.81, -0.16, -0.54, 0.29},
    {0.23, -0.28, 0.44, 0.91}, {-0.69, 0.33, -0.26, 0.48}, {0.73, -0.89, -0.45, 0.60},
    {-0.88, 0.76, 0.51, 0.42}, {0.55, -0.73, -0.61, 0.93}, {0.21, 0.50, 0.68, -0.77},
    {0.16, -0.24, 0.61, 0.37}, {-0.74, 0.52, -0.60, 0.11}, {0.92, -0.82, -0.49, 0.17},
    {-0.45, 0.57, 0.79, 0.63}, {0.38, -0.15, 0.87, -0.23}, {-0.53, 0.39, -0.22, 0.16},
    {0.24, -0.34, 0.63, 0.52}, {-0.12, 0.18, -0.93, -0.41}, {0.68, -0.28, 0.16, 0.75},
    {-0.67, 0.41, -0.08, -0.93}, {0.59, 0.72, -0.36, 0.14}, {0.26, -0.59, 0.53, 0.22},
    {-0.47, 0.31, 0.69, -0.45}, {0.10, 0.28, 0.85, -0.27}, {-0.63, 0.45, -0.77, 0.40},
    {0.84, -0.19, 0.44, 0.62}, {-0.81, 0.56, -0.50, 0.28}, {0.34, -0.61, 0.62, -0.74},
    {0.21, 0.43, -0.88, 0.55}, {-0.55, -0.39, 0.44, -0.29}
};

const double bias_hidden[4] = {0.1, -0.2, 0.05, 0.3};
const double weights_output[4] = {0.6, -0.4, 0.7, -0.9};
const double bias_output = 0.2;

double neural_network(double input[32]) {
    double hidden_layer[4];
    for (int i = 0; i < 4; i++) {
        hidden_layer[i] = bias_hidden[i];
        for (int j = 0; j < 32; j++) {
            hidden_layer[i] += input[j] * weights_hidden[j][i];
        }
        hidden_layer[i] = sigmoid(hidden_layer[i]);
    }

    double output = bias_output;
    for (int i = 0; i < 4; i++) {
        output += hidden_layer[i] * weights_output[i];
    }
    return sigmoid(output);
}

void caesar_shift(char* str, int key) {
    for (int i = 0; i < strlen(str); i++) {
        str[i] = str[i] + key;
    }
}

int main() {
    FILE* f = fopen("flag.txt", "rb");
    if (!f) {
        printf("Missing flag.txt file\n");
        return 1;
    }

    double input[32];
    printf("Enter 32 numbers:\n");
    for (int i = 0; i < 32; i++) {
        if (scanf("%lf", &input[i]) != 1) {
            printf("Invalid input.\n");
            return 1;
        }
    }

    double result = neural_network(input);
    int key = (int)(result * 100);

    char cybernight[] = "CYBERNIGHT2025";
    caesar_shift(cybernight, key);

    char decrypted[128];
    int ch, i = 0;

    while ((ch = fgetc(f)) != EOF && i < sizeof(decrypted) - 1) {
        decrypted[i] = (ch ^ cybernight[i % strlen(cybernight)]);
        i++;
    }
    decrypted[i] = 0;
    fclose(f);

    if (strncmp(decrypted, "CYBN{", 5) == 0) {
        printf("Flag: %s\n", decrypted);
    } else {
        printf("Incorrect input. ACCESS DENIED.\n");
    }

    return 0;
}