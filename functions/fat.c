#include <stdio.h>

int fat(int number);

int fat(int number){
	if (number < 0)
		return 0;
	if (number == 1 || number == 0) 
		return 1;
	else 
		return number*fat(number-1);
}

