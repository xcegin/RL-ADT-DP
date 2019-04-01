#include <stdio.h>
#include "three_digits.h"

int three_digits(int n);

int three_digits(int n)
{
    int r, d = 0, p=1, i=0;

    for(i=0; i<3; i++)
    {
        r = n%10;
        d += r * p;
        p *= 10;
        n /= 10;
    }
    return d;
}
