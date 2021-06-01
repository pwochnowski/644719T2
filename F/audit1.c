/*
  elem is of type int* whereas storage is a char array, this means
  that incrementing elem by 1 is the same as incrementing storage by 4
  so after 32/4 = 8 increments we will have reached the end of the array
  and since this means that after a few more iterations we reach the return address
  we effectively have control of the instruction pointer.
*/

#include <stdio.h>
int main() {
    char storage[32] = {0};

    int len = 0;
    puts("How many chars would you like to store?");
    scanf("%d", &len);

    if (len >= 32) {
        printf("no");
        return 1;
    }

    int i = 0;
    int *elem = storage;
    for(; i < len; i++, elem++) {
        printf("Enter character %d: ", i);
        scanf("%d", elem);
    }
}
