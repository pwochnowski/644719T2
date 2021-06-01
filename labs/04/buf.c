#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BUF_SIZE 1024
int main(int argc, char * argv[]){
  char buf[BUF_SIZE];

  static int test_val = 0x00414141; //"AAA\0" as an int


  strncpy(buf, argv[1], BUF_SIZE);

  printf("Right: ");
  printf("%s", buf);//<------safe
  printf("\n\n");

  printf("Wrong: ");
  printf(buf);      //<------vulnerable
  printf("\n\n");

  printf("[*] test_val @ %p = %d 0x%08x\n", &test_val,test_val,test_val);

  exit(0);

}
