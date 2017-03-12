#include <stdio.h>
#include <cs50.h>
#include <string.h>
#define MAXLENGTH 16 //defining constants
int main(void)
{
   
   printf("Please type in your card number.");
   long long cardNumber=GetLongLong();
   
   //stores input cardNumber into the char array aka string (sprintf: It kinda means data transferring)
   char s[MAXLENGTH];
   sprintf(s, "%lld", cardNumber);
   int len = strlen(s);
   
   //validity checking
   if(len<13||len > 16||len ==14)
   {
     printf("INVALID\n");
     return 0; 
   }
   
   //converting string array into integer array for easier processing(i.e. changing "123456789" to 123456789)
   //(e.g. if the number in the string is '6','6'-'0'will yield 6, type int. P.S. because ASCII value for string 6 is 54 and for string 0 is 48)
   int number[len];
   for(int i=0; i < len; i++)
   {
      number[i] = s[i] - '0';
   }
   int sum = 0, k=1;
   for(int j = len - 1; j >= 0; j--)
   {
      if(k % 2 == 0)
      {
        sum = sum + number[j] * 2;
        if(number[j] * 2 >= 10)
           sum++;
      }
      else
          sum=sum+number[j];
      k++;     
   }
   
   if(number[0] == 3 && (number[1] == 4||number[1] == 7) && sum % 10 == 0)
       printf("AMEX\n");
   else if (number[0] == 5 && number[1] > 0 && number[1] < 6 && sum % 10 == 0)
       printf("MASTERCARD\n");
   else if (number[0]== 4 && sum % 10 == 0)
       printf("VISA\n");
   else
       printf("INVALID\n");
   
   
   return 0 ;
}

