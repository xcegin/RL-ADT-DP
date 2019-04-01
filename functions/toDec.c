/*
 * convert from any base to decimal
 */

#include <stdio.h>

int toDec(int number, int base);

int toDec(int number, int base) {
	int i;
	
	
	if ( number >= 48 && number <= 57 )
		number -= 48;
	else if ( number >= 65 && number <= 90 )
		number -= 65 - 10;
	else if ( number >= 97 && number <= 122 )
		number -= 97 - 10;
	else
		number = base + 1;

	if (number > base)
		return 0;
	return 1;
}
