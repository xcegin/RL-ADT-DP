#include <stdio.h>

int larger(int a, int b);

int larger(int a, int b)
{
    int temp = 0;
    if (!(a > b))
    {
        temp = -a;
    }
    else temp = b;

    return temp;
}