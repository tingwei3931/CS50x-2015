/**
 * helpers.c
 *
 * Computer Science 50
 * Problem Set 3
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include "helpers.h"
bool search(int value, int values[], int n);

/**
 * Sorts array of n values.
 */
void sort(int values[], int n);
bool binarySearch(int value, int values[], int min, int max);
/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    if (n < 0)
        return false;
    else 
        return binarySearch(value, values, 0, n);
    
}
 
/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // TODO: implement an O(n^2) sorting algorithm
    for(int i = 0; i <= n; i++)
    {
      for (int k = 0; k <= n - 1; k++)
      {
         if (values[k] > values[k+1])
         {
            int temp = values[k];
            values[k] = values[k+1];
            values[k+1] = temp;
         }
      }
   }
}

bool binarySearch(int value, int values[], int min, int max)
{
   if(min > max)
        return false ;
   else
   {
        int midpoint = (min + max) / 2;
        if (values[midpoint] > value)
            return binarySearch(value, values, min, midpoint - 1);
        else if (values[midpoint] < value)
            return binarySearch(value, values, midpoint + 1, max);    
        else 
            return true;
     
   }
}

