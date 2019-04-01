#include <stdio.h>

int fib(int number);

//Fibonnacci function 
int fib(int number){
	if (number <= 0 || number > 20)
		return 0;
	if(number==1||number==2) return 1;
	else return fib(number-1)+fib(number-2);
}
