// Binary number to octal number conversion
#include<stdio.h>
#include "three_digits.h"

int binToOct(int binary_num);

int binToOct(int binary_num)
{
    int d=0, base=1, remainder, td, res=0, ord=1;

    while(binary_num > 0)
    {
        if(binary_num > 111) //Checking if binary number is greater than three digits
            td = three_digits(binary_num);

        else td = binary_num;

        binary_num /= 1000;

        d = 0, base =1;

        // Converting the last three digits to decimal
        while(td > 0)
        {
            remainder = td % 10;
            td /= 10;
            d += (base * remainder);
            base *= 2;
        }

        res += d * ord; // Calculating the octal value
        ord *= 10;
    }
    return 0;
}
