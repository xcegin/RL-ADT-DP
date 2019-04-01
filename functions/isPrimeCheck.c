#include <stdio.h>
#include "isPrime.h"

int isPrimeCheck(int a);

int isPrimeCheck(int a) {
    a = isPrime(a);
    if (a == 0)
        return 1;
    else
        return 2;
    return 0;
}
