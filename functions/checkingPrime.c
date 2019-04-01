#include <stdio.h>
#include "checkPrime.h"

int checkingPrime(int n);

int checkingPrime(int n)
{
    int i, flag = 0;

    for(i = 2; i <= n/2; ++i)
    {
        // condition for i to be a prime number
        if (checkPrime(i) == 1)
        {
            // condition for n-i to be a prime number
            if (checkPrime(n-i) == 1)
            {
                // n = primeNumber1 + primeNumber2
                flag = 1;
            }

        }
    }

    if (flag == 0)
        return;

    return 0;
}
