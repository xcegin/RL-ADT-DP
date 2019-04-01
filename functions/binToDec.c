/**
 * Modified 07/12/2017, Kyler Smith
 * 
 */

#include <stdio.h>

void binToDec(int number);

void binToDec(int number) {

	int remainder, decimal_number = 0, temp = 1;

	// Iterate over the number until the end.	
	while(number > 0) {
	
		remainder = number % 10;
		number = number / 10;
		decimal_number += remainder * temp;
		temp = temp*2;		//used as power of 2
	
	}
}
