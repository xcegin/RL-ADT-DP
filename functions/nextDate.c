#include <stdio.h>

int nextDate(int year, int month, int day);

int nextDate(int year, int month, int day)
{
	int leap_year = 0;
	int month_length = 0;
	if (year < 0 || month < 1 || day < 1){
		return -1;
	}
	else {
		//year
		if (year % 400 == 0 || year % 4 == 0){
			leap_year = 1;
		}
		else {
			if (year % 100 == 0){
				leap_year = 0;
			}
			else {
			leap_year = 0;
			}
		}
		//month
		if (month == 1 || month == 3 || month == 5 || month == 7 || month == 8)
		{
			month_length = 31;
		}
		else{
			if (month == 2) {
				if (leap_year == 1) {
					month_length = 29;
				}
				else {
					month_length = 28;
				}
			}
			else {
				month_length = 30;
			}
		}
		//day
		if (day < month_length)
		{
			day = day + 1;
		}
		else {
			day = 1;
			if (month == 12){
				month = 1;
				year = year + 1;
			}
			else {
				month = month + 1;
			}
		}
	}
	return 0;
}
