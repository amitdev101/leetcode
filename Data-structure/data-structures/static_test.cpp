#include<bits/stdc++.h>
using namespace std;
#define watch(x) cout<<(#x)<<" = "<<x<<" \t"

void static_test(){
    static int i=5; // it is only defined once. so during recursion it will retain it's previous value
                // and will not initialize again to 5
    int x = 5;
    watch(i);
    watch(x);
    i++;
    x++;
}

int main(){
    for(int i=0;i<5;i++)
    // for(int j=0;j<5;j++)
    {
        static_test();
        watch(i); cout<<"\n";

    }
    // output: i = 5 	x = 5 	i = 6 	x = 5 	i = 7 	x = 5 	i = 8 	x = 5 	i = 9 	x = 5 	
    return 0;
}