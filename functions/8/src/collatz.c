/*
collatz conjecture: a series for a number n in which if n even then the next number is n/2 ,but if n is odd then the next number is 3n+1.
this series continues till it reaches 1*/

#include<stdio.h>

int collatz(int curr_no);

int collatz(int curr_no)
{     //curr_no stores input number n
    while(curr_no!=1 && curr_no > 0)     //loop till series reaches 1
    {
        if(curr_no%2==0)      //condition   for even number
        {
            curr_no=curr_no/2;
        }    
        else 
        {
            curr_no=(curr_no*3)+1;      //condition for odd number
        }
    }
    return 0;
}
