#include<stdio.h>

int Calc (int x, int y, int z);

int Calc (int x, int y, int z) {
int result = -1;

if (x < 0 || y < 0 || z < 0 ) {
	return -1 ; //illegal parameter value
}

if (x >= 0 || y >= 0 || z >= 0 ) {

	if (z == 0 ) {
		result = x + y;
	}
	else {
		if (z > x && z > y) {
			y = x + y;
			if (z > x)
			{
				result = z;
			}
		}
		else {
			result = x + y;
		}
	}
}

return result;
}

