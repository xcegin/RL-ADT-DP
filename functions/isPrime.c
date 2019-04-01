#include <stdio.h>
#include "isPrime.h"

int isPrime(int x);

int isPrime(int x) {
	int i = 2;
    for (i = 2; i < x / 2; i++) {
        if (x%i == 0)
            return 0;
    }
    return 1;

}
