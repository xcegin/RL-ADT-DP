#include <stdio.h>

int palindrome(int n, int originalInteger);

int palindrome(int n, int originalInteger)
{
    int reversedInteger = 0, remainder;

    originalInteger = n;

    // reversed integer is stored in variable 
    while( n!=0 )
    {
        remainder = n%10;
        reversedInteger = reversedInteger*10 + remainder;
        n /= 10;
    }

    // palindrome if orignalInteger and reversedInteger are equal
    if (originalInteger == reversedInteger)
        return 1;
    else
        return 2;
    
    return 0;
}
