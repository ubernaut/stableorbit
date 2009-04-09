/****************************************************************/
/*Program: PARSE.C                                              */
/*Author:  Alexander A.K.A Xenofied                                */
/*Platform: Windows Operating System(tested on XP PIII, PIV, PM)*/
/*Compiler: Free Dev-C++ Compiler (@ http://www.bloodshed.com/) */
/*Comment: Program to read in a sentence of words within a file */
/*         and parse them into seperate lines of words.         */
/****************************************************************/

#include <stdio.h>   /*All c program must have this*/
#include <string.h>
#define bufsize 1024 /*A defined integer for our buffer size*/
using namespace std;



int main(){          /*Program entry point*/
  FILE* p_file;       /*Declare file pointer variable*/
  char * pch;
  char buffer [400];
  int i;
  float f;
  
  p_file = fopen("initial_conditions.txt", "r");
  while ( ! feof (p_file) )
  {
    pch = fgets (buffer , 400 , p_file);
    pch = strtok(buffer," ");
    while (pch != NULL)
    {
      printf ("%s\n",pch);
      pch = strtok (NULL, " ");
      f = sscanf(pch, "%f", &f);
    }
    
    
  }
  
  
  return 0; /*Executed without errors*/
}

