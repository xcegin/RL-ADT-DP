#include <stdio.h>
#include <stdlib.h>

int decimal2bin(int inputNumber);

int decimal2bin(int inputNumber)
{


    // for the remainder
    int re;

    // contains the bits 0/1
    int bits;

    // for the loops
    int j;
    int i=0;

    // make sure the input number is a positive integer.
    if (inputNumber < 0)
    {
        return 1;
    }

    // actual processing
    while(inputNumber>0)
    {

        // computes the remainder by modulo 2
        re = inputNumber % 2;

        // computes the quotient of division by 2
        inputNumber = inputNumber / 2;

        bits = re;
        i++;

    }


    return 0;
}

