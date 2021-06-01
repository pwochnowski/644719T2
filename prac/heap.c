#include<stdlib.h>

int main() {

  void* a = malloc(10);     // 0xa04010
  void* b = malloc(10);     // 0xa04030
  void* c = malloc(10);     // 0xa04050

  free(a);
  free(b);  // To bypass "double free or corruption (fasttop)" check
  free(a);  // Double Free !!

  void* d = malloc(10);     // 0xa04010
  void* e = malloc(10);     // 0xa04030
  void* f = malloc(10);     // 0xa04010   - Same as 'd' !
}
