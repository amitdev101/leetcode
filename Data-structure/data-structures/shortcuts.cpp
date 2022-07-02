#include<iostream>
using namespace std;

// print a variable with simple command without writing name of variable
#define print(x) cout<<(#x)<<" is "<<x<<"\n"

int main(){
    int x=1,y=2;
    char str[] = "hello";
    print(x);
    print(y);
    print(str);

    
    return 0;
}