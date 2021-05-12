#include<bits/stdc++.h>
using namespace std;
double findMedianSortedArrays(vector<int> &a, vector<int> &b) {
    int m = a.size(), n = b.size();
    if (m > n) {
        swap(m, n);
        swap(a, b);
    }
    
    int halfLen = (m + n + 1)/2;
    int l = 0, h = m;
    int maxLeft, minRight;

    while (l <= h) {
        int mid = (l+h)/2;
        int j = halfLen - mid;

        if (mid < m && b[j-1] > a[mid]) {
            l = mid+1;
        }
        else if (mid > 0 && a[mid-1] > b[j]) {
            h = mid-1;
        }
        else {
            // perfect partition
            if(mid == 0) {
                maxLeft = b[j-1];
            }
            else if(j == 0) {
                maxLeft = a[mid-1];
            }
            else {
                maxLeft = max(a[mid-1], b[j-1]);
            }

            if((m+n)%2 == 1)    return maxLeft;

            if(mid == m) {
                minRight = b[j];
            }
            else if(j == n) {
                minRight = a[mid];
            }
            else {
                minRight = min(a[mid], b[j]);
            }

            return (maxLeft + minRight) / 2.0;
        }
    }
    return 0;
}