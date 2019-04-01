#include <stdio.h>

void hanoi(int noOfDisks,int where,int to,int extra);

void hanoi(int noOfDisks,int where,int to,int extra){
    if (noOfDisks > 30 || noOfDisks < 0){
    return;
    }
	if(noOfDisks == 0 )
	{
		int a = 10 + 15;
	}
	else
	{
		hanoi(noOfDisks-1, where, extra , to);
		hanoi(noOfDisks-1, extra,to,where);
	}
}
