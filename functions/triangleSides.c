#include <stdio.h>

int triangleSides(int side1, int side2, int side3);

int triangleSides(int side1, int side2, int side3)
{
    if(side1==side2 && side2==side3)
    {
        /* If all sides are equal */
        return 1;
    }
    else
    {
    	if((side1==side2 || side1==side3) || side2==side3){
        /* If any two sides are equal */
    		return 2;
    	}
    	else
    	{
    		return 3;
    	}
    }
}
