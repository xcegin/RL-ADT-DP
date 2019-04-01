#include<stdio.h>

void strng(int a);

void strng(int a)
{
	int j=a;
	int b;
	int sum=0;
	int fact=1;
	while(a>0)
	{
		fact=1;
		b=a%10;
		for(int i=1;i<=b;i++)
		{
			fact=fact*i;
		}
		a=a/10;
		sum=sum+fact;
	}
	if(sum==j)
		j=1;
	else
		j=0;
}

