/*****Decimal to octal conversion*******************/
#include <stdio.h>

void decimal2Octal(long quotient);

void decimal2Octal(long quotient){
  long remainder;

    int octalNumber, i = 1, j;

    while (quotient != 0){
		octalNumber = quotient % 8;

        quotient = quotient / 8;
	}

}
