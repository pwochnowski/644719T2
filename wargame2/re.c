#include<stdio.h>

int main(int argc, char** argv, const char** envp()) {
  int n;
  n = scanf("%d\n", &n);
  if (n != 0x539) {
    puts("Bye");
  } else {
    puts("Your so leet!");
  }
}

