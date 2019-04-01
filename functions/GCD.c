#include <stdio.h>

int GCD(int x, int y);

// Euclid's algorithm
int GCD(int x, int y) {
    if (y == 0)
        return x;
    return GCD(y, x%y);
}
