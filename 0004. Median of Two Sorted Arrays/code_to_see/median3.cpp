double findMedianSortedArrays(int A[], int B[]) {
    int n = A.length;
    int m = B.length;
    // the following call is to make sure len(A) <= len(B).
    // yes, it calls itself, but at most once, shouldn't be
    // consider a recursive solution
    if (n > m)
        return findMedianSortedArrays(B, A);

    // now, do binary search
    int k = (n + m - 1) / 2;
    int l = 0, r = Math.min(k, n); // r is n, NOT n-1, this is important!!
    while (l < r) {
        int midA = (l + r) / 2;
        int midB = k - midA;
        if (A[midA] < B[midB])
            l = midA + 1;
        else
            r = midA;
    }
    
    // after binary search, we almost get the median because it must be between
    // these 4 numbers: A[l-1], A[l], B[k-l], and B[k-l+1] 

    // if (n+m) is odd, the median is the larger one between A[l-1] and B[k-l].
    // and there are some corner cases we need to take care of.
    int a = Math.max(l > 0 ? A[l - 1] : Integer.MIN_VALUE, k - l >= 0 ? B[k - l] : Integer.MIN_VALUE);
    if (((n + m) & 1) == 1)
        return (double) a;

    // if (n+m) is even, the median can be calculated by 
    //      median = (max(A[l-1], B[k-l]) + min(A[l], B[k-l+1]) / 2.0
    // also, there are some corner cases to take care of.
    int b = Math.min(l < n ? A[l] : Integer.MAX_VALUE, k - l + 1 < m ? B[k - l + 1] : Integer.MAX_VALUE);
    return (a + b) / 2.0;
}