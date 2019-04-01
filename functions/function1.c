#include <stdio.h>

void function1(int a, int b);

void function1(int a, int b)
{
	int x = 1, y = 2;

	if (0 != a)
	{
		y += 3 + x;
		if (0 == b)
		{
			x = 2 * (a + b);
		}
	}

	if (1 != a)
	{
		y = 5;
	}
	else
	{
		y = 6;
	}
}