#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char* argv[])
{ 
    string name;
    name = GetString();
    //if the input doesnt give error
    if (name != NULL)
    {
      //print the first character to be uppercase
      printf("%c", toupper(name[0]));
      //iterate through the loop to find the character after a space and capitalizes it
      for (int i = 0, n = strlen(name); i < n; i++)
      {
        if (name[i] == ' ')
        {
            printf("%c", toupper(name[i+1]));
        }
      }   
      printf("\n");
    }
    else
        return 1;
}
