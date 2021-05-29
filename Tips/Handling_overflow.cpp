// this will handle 32bit range and check whether the number is overflowing.
if (base > INT_MAX / 10 || (base == INT_MAX / 10 && str[i] - '0' > INT_MAX % 10))
