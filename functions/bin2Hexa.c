/*
 * C Program to Convert Binary to Hexadecimal 
 */
#include <stdio.h>

int bin2Hexa(int binary);
 
int bin2Hexa(int binary)
{
    int hexa = 0, i = 1, remainder;
    while (binary != 0)
    {
        remainder = binary % 10;
        hexa = hexa + remainder * i;
        i = i * 2;
        binary = binary / 10;
    }
    return 0;
}
