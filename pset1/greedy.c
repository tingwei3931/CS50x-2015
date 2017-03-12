#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float amount;
    int amountInCent;
    int quarter = 25;
    int dime = 10;
    int nickel = 5;
    int penny = 1;
    int count = 0;
    //getting input for the amount of change
    do
    {
        printf("O hai! How much change is owed?\n");
        printf("change: ");
        amount=GetFloat();
    }while(amount < 0);
    
    //rounding off the value input to avoid floating point imprecision and convert it to cents by multiplying with 100
    amountInCent=(int)roundf(amount*100);
    while (amountInCent >= quarter)
    {
        amountInCent = amountInCent - quarter;
        count++;
    }
    while (amountInCent >= dime)
    {
        amountInCent = amountInCent - dime;
        count++;
    }
    while (amountInCent >= nickel)
    {
        amountInCent = amountInCent - nickel;
        count++;
    }
    while (amountInCent >= penny)
    {
        amountInCent = amountInCent - penny;
        count++;
    }
    printf("%d\n",count); 
}   
