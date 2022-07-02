// Applying mergesort method
#include<iostream>
using namespace std;
#define watch(x) cout<<(#x)<<" is "<<x<<"\n"
#define print(x) cout<<x<<"\n"

void merge(int arr[], int start, int mid, int end)
{
    //stores the starting position of both parts in temporary variables.
    int p = start;
    int q = mid + 1;
    int k = 0; // temparr index
    int temparr[end - start + 1]; // take example (n-1 -0 + 1) = n elements

    for (int i = start; i <= end; i++){
        if (p > mid) //checks if first part comes to an end or not .
            temparr[k++] = arr[q++];

        else if (q > end) //checks if second part comes to an end or not
            temparr[k++] = arr[p++];

        else if (arr[p] < arr[q]) //checks which part has smaller element.
            temparr[k++] = arr[p++];

        else // second array has smaller element. so adding this to temparr.
            temparr[k++] = arr[q++];
    }

    for (int p = 0; p < k; p++)
    {
        /* Now the real array has elements in sorted manner including both 
        parts.*/
        arr[start++] = temparr[p];
    }
}

void merge_sort(int arr[], int start, int end)
{
    if (start < end)
    {
        int mid = (start + end) / 2; // defines the current array in 2 parts .
        merge_sort(arr, start, mid);   // sort the 1st part of array .
        merge_sort(arr, mid + 1, end); // sort the 2nd part of array.

        // merge the both parts by comparing elements of both the parts.
        merge(arr, start, mid, end);
    }
}

void print_arr(int arr[],int n){
    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<"\n";
}

int main(){
    int arr[]={-1,1,0,-8,99,2,9,9,7,1,2,3};
    int n = sizeof(arr)/sizeof(int);
    print_arr(arr,n);
    merge_sort(arr,0,n-1);
    print_arr(arr,n);
    return 0;
}