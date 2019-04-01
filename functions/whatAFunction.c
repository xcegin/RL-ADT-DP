#include<stdio.h>

int whatAFunction(int sum, int n, int num);

int whatAFunction(int sum, int n, int num)
{
	int i;
	while (n!=0)
	{
		i=n%10;
		sum=sum+(i*i*i);
		n=n/10;
	}
	if (sum==num)
	{
		return 1;
	}
	else
	{
		return 2;
	}
	return 0;
}
