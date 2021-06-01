char * array; // defined somewher

// this could return either int or void
void f() {
  int pos = 0;
  char c = getchar();
  bool done = 0;
  while (!done) {
    switch (c) {
      case('P'):
        putchar(array[pos]);
        break;
      case('U'):
        pos = (pos + 1) % 27;
        break;
      case('U'):
        pos = (pos - 1) % 27;
        break;
      default:
        done = 1;
    }
  }
  putchar('\n');

  // this might not be in the function its ambiguous
  return 0;
}