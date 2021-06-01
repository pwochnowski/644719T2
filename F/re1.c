struct hdr {
  // anything of size 4
  int padding;
  char *s1;
  char *s2;
};

int f(int n, struct hdr* hdr) {
  if (n == 3) {
    long l = strtol(hdr->s1, 0, 10);
    l += strtol(hdr->s2, 0, 10);
    if (l == (int) htons(0x11BB)) {
      return 1;
    }
  }
  return 0;
}
