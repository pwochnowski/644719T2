double sumDifference(float *arr1, float *arr2) {
  float* v1 = arr1;
  float* v2 = arr2;
  float sum = 0.0;
  while (arr1 != NULL) {
    sum += *arr1 - *arr2;
    arr1++;
    arr2++;
  }
  return sum;
}