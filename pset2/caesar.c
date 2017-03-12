#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char* argv[])
{
  int k;
  string text;
  if(argc == 1)
  {
   printf("Invalid command line argument. The program will now exit.");
   return 1;
  }
  //if command-line argument consists of two strings, continue the program, if not return 1 to exit the program.
  else if (argc == 2)
  {
  //the secret key can be more than 26, the code section below processes the key so that k = 27 will also yield the same 
  //result with k = 1 because the key loops back cyclically
    if(atoi(argv[1]) > 26)
    {
      k = atoi(argv[1]);
      k = k % 26;
    }
    else
    {
      k = atoi(argv[1]);
    }
    //getting input from user
    text = GetString();
    //processing the input by accessing each character
    for(int i = 0, n = strlen(text); i < n; i++)
    {
     //the program only encrypts alphabets and ignores numbers and other symbols
     if(isalpha(text[i]))
     {
      // if the letter is uppercase, the ascii value of that character is subtracted by 65 to scale it down to 1-26 and add
      // the result to the key. If the sum exceeds 26, the loop executes again and finally scale it up back to its original ascii value
      if(isupper(text[i]))
      {
       printf("%c",((text[i] - 65) + k) % 26 + 65);
      }
      //the same thing is done to lowercase letters except the number used is 97 because ascii value of 'a' starts with 97 
      else
      {
       printf("%c", ((text[i] - 97) + k) % 26 + 97);
      }
     }
     //other characters like symbols and numbers are ignored and printed out the way they are in the input
     else
       printf("%c", text[i]);
    }
    printf("\n");
    return 0;
  }
  //if the command line argument contains more than 2 strings, the program ends
  else
      return 1;
}
