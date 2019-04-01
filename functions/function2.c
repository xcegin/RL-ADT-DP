#include <stdio.h>

void function2(int a);

void function2(int a)
{
	int x = a;
	x++;
	int y = x++ + 3;
	int z = --x + 4;

	if (z & 1)
	{
		a = 50;
	}
}
