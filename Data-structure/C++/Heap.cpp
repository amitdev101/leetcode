#include<iostream>
using namespace std;
#define capacity 100005
int minheap[capacity];
int size = 0;

void myswap(int *a,int *b){
    int temp=*a;
    *a = *b;
    *b = temp;
}

void bubble_up(int i){
    // replace current index with parent if current index is smaller than the parent
    int p = (i-1)/2;
    if(minheap[i]<minheap[p]){
        myswap(&minheap[i],&minheap[p]);
        bubble_up(p);
    }
}

void insert(int key){
    minheap[size++]=key;
    int index = size-1;
    bubble_up(index);
}

void minheapify(int pi){
    // now compare it with other elements;
    int l = 2*pi + 1;
    int r = 2*pi + 2;
    int smallest = pi;
    if(l<size && minheap[l]<minheap[smallest])
        smallest = l;
    if(r<size && minheap[r]<minheap[smallest])
        smallest = r;
    if(smallest!=pi){
        myswap(&minheap[smallest],&minheap[pi]);
        minheapify(smallest);
    }
     
}

int extract_min(){
    int ans;
    if(size>0){
        ans = minheap[0];
        minheap[0]=minheap[size-1];
        size--;
        minheapify(0);
    }
    return ans;
}

void heapsort(int arr[],int n){
    //size = n
    for(int i=0;i<n;i++){
        insert(arr[i]);
    }
    for(int i=0;i<n;i++){
        arr[i]= extract_min();
    }
}

void print(int arr[],int n){
    for(int i=0;i<n;i++){
        cout<<arr[i]<<" ";
    }
    cout<<"\n";
}

int main(){
    int arr[] = {1,0,-1,-3,-4,5,99,2,1,2};
    int n = sizeof(arr)/sizeof(int);
    heapsort(arr,n);
    print(arr,n);

    return 0;
}
