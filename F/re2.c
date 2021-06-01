// Assume ebp+s refers to the second argument as
// it is used without initalizing (so unlikely to be local)
// AND it is indexed of the base pointer (so unlikely to be global)
int sumDifference(char* s1, char* s2) {
  int i = 0;
  int sum = 0;
  while (i != strlen(s2)) {
    sum += s2[i] - s1[i];
  }
  return sum;
}