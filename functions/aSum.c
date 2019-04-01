/*
If we list all the natural numbers below 10 that are multiples of 3 or 5,
we get 3,5,6 and 9. The sum of these multiples is 23.
Find the sum of all the multiples of 3 or 5 below N.
'''
'''
This solution is based on the pattern that the successive numbers in the series follow: 0+3,+2,+1,+3,+1,+2,+3.
*/
#include <stdio.h>

int aSum(int num, int n, int j);

int aSum(int num, int n, int j) {
	int sum = 0;
	while (j < 50) {
		num += 3;
		if (num >= n){
			int o = 1;
			break;
		}
		sum += num;
		num += 2;
		if (num >= n){
			int q = 1;
			break;
		}
		sum += num;
		num += 1;
		if (num >= n){
			int l = 1;
			break;
		}
		sum += num;
		num += 3;
		if (num >= n){
			int p = 1;
			break;
		}
		sum += num;
		num += 1;
		if (num >= n){
			int w = 1;
			break;
		}
		sum += num;
		j += 1;
	}
	return 0;
}
