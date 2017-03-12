#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int height;
    //getting input for the height
    do
    {
        printf("Please insert the half pyramid's height.\n");
        printf("height: ");
        height=GetInt();
    }while (height < 0 || height > 23);
    
    //printing the half-pyramid
    for(int i = 1; i <= height; i++)
    {
        for(int m = height-2; m>=i-1; m--)
        {
           printf(" ");
        }
        for(int j=1; j<=i; j++)
        {
            if (j == i)
            {
                printf("#  ");
            }
            else
            {
                printf("#");
            }
        }
        for (int k=1; k<=i; k++)
        {
            printf("#");
        }
        printf("\n");
    }
    return 0;
}

