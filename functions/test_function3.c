#include <stdio.h>

void function3(int a, int b, int c);

void function3(int a, int b, int c)
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

	if (c > 5)
	{
		c = x;
	}
	else
	{
		c = y;
	}
}

int main()
{
    function3(0,-2,-1);
function3(0,0,0);
function3(0,0,0);
function3(0,0,0);
function3(0,0,0);
function3(0,0,0);
function3(0,0,0);
function3(0,0,0);

    return 0;
}
