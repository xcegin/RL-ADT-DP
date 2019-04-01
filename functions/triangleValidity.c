#include <stdio.h>

int triangleValidity(int angle1, int angle2, int angle3);

int triangleValidity(int angle1, int angle2, int angle3)
{

    /*
     * If sum of angles is 180 and
     * angle1, angle2, angle3 is not 0 then
     * triangle is valid.
     */
    if(angle1 != 0 && angle2 != 0 && angle3 != 0)
    {
    	angle1 = angle1 + angle2 + angle3;
    			if (angle1 == 180){
					return 1;
    			}
    }

    return 0;
}
