/*
code for computing nth catalan number
*/
#include<stdio.h>

long int catalan(int x);

long int catalan(int x)    //long int for more than 10 factorial
{
     long int fac;   //fac stores x factorial  
     fac=x;
     for(int i=1;i<x;i++)    //loop to calculate x factorial
     {
        fac=fac*(x-i);
     }
     return fac;   //returning x factorial
}

