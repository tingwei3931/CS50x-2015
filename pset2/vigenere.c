#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <cs50.h>

int main(int argc, char* argv[])
{
    char finaltext;
    string key;
    string text;
    int length;
    //argc must be two or the program will exit
    if(argc != 2)
    {
       printf("This program only accepts two command-line arguments");
       return 1;
    }
    
    //moving argv[1] to key for easier processing
    key = argv[1];
    length = strlen(key);
  
    //check for invalid characters in the key
    for(int i = 0; i < length; i++)
    {
      if (!isalpha(key[i]))
      {
        printf("Invalid characters in argument.\n");
        return 1;
      }
    } 
    //let user input the original text
    text = GetString();
  
      
    for(int i = 0, t = 0, n = strlen(text); i < n; i++, t++)
    {
       //if key is shorter than original text, the key is cycled again 
       if (t >= length)
       {
         t = 0;
       }
    
       //skips the character in the text which are not alphabets
       if (!isalpha(text[i]))
       {
         t--;
       }
       
       //scales down the key into a range of 0-25 (P.S. lowercase and uppercase contains the same number i.e. A/a = 0)   
       if (isupper(key[t]))
       {
          key[t] = key[t] - 'A'; 
       }
       else if (islower(key[t]))
       {
          key[t] = key[t] - 'a';
       }
       
       //if text[i] is uppercase
       if (isupper(text[i]))
       {
          finaltext = text[i] - 'A';
          finaltext = ((finaltext + key[t]) % 26) + 'A';
          printf("%c", finaltext);
       }
       //if text[i] is lowercase
       else if(islower(text[i]))
       {
          finaltext = text[i] - 'a';
          finaltext = ((finaltext + key[t]) % 26) + 'a';
          printf("%c", finaltext);
       }
       else
       //print the remaining text
       {
          printf("%c",text[i]);
       }
    }
    printf("\n");
    return 0;
}

    
