#include <bits/stdc++.h>
using namespace std;
struct Person
{
    int Age;
    float Height;
    // this will used to initialize the variables
    // of the structure
    Person(int age, float height) : Age(age), Height(height)
    {
    }
};

// this is an structure which implements the
// operator overloading
struct CompareHeight
{
    bool operator()(Person const &p1, Person const &p2)
    {
        // return "false" if "p1" is ordered
        // before "p2", for example:
        if(p1.Height > p2.Height){
            return false;
        }
        return true;
    }
};

void general_heap_test();

int main()
{
    priority_queue<Person, vector<Person>, CompareHeight> Q;
    

    // When we use priority_queue with  structure
    // then we need this kind of syntax where
    // CompareHeight is the functor or comparison function
    int ROW = 5, COL = 3;
    float arr[ROW][COL] = {{30, 5}, {25, 5}, {20, 5}, {33, 6.1}, {23, 5.6}};

    for (int i = 0; i < ROW; ++i)
    {

        Q.push(Person(arr[i][0], arr[i][1]));

        // insert an object in priority_queue by using
        // the Person structure constructor
    }

    while (!Q.empty())
    {
        Person p = Q.top();
        Q.pop();
        cout << p.Age << " " << p.Height << "\n";
    }
    general_heap_test();
    return 0;
}

void general_heap_test(){
    // making heap for integers
    struct compare{
        bool operator() (int a, int b){
            // return false if you want to put a before b
            // let's build a maxheap
            if(a>b){
                return false;
            }
            return true;
        }
    };

    int arr[] = {-1,2,3,4,-5,6,};
    priority_queue<int,vector<int>,compare> maxheap;
    for(int i=0;i<6;i++){
        maxheap.push(arr[i]);
    }
    while(!maxheap.empty()){
        int temp;
        temp = maxheap.top();
        maxheap.pop();
        cout<<temp<<"\n";
    }
}