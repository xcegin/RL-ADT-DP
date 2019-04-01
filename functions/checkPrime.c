#include <stdio.h>
#include "checkPrime.h"

int checkPrime(int n);

// Function to check prime number
int checkPrime(int n)
{
    int i, isPrime = 1;

    for(i = 2; i <= n/2; ++i)
    {
        if(n % i == 0)
        {
            isPrime = 0;
            break;
        }
    }

    return isPrime;
}
