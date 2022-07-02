#include<iostream>
using namespace std;

#define watch(x) cout<<(#x)<<" is "<<x<<"\n"
#define print(x) cout<<x<<"\n"
#define stackcapacity 100

struct Stackdata{
    // data to be stored in stack 
    int data; 
    // Node* nodeptr; // This is just for example;
};

struct Stack{
    Stackdata arr[stackcapacity];
    // if you want to allocate memory with malloc then you can store a pointer.
    // And then set this pointer to the pointer returned by malloc function.
    // Stackdata* ptr; (now in init function write ptr=(Stackdata*)malloc(sizeof(Stackdata*capacity)))
    int top;
    int size;
    int maxsize;
};

Stack* getnewstack(){
    Stack* stackptr;
    stackptr = (Stack*)malloc(sizeof(Stack));
    stackptr->top=0;
    stackptr->size=0;
    stackptr->maxsize=stackcapacity;
    return stackptr;
}

int isempty(Stack* stackptr){
    if(stackptr->size==0){
        return 1;
    }
    return 0;
}

int isfull(Stack* stackptr){
    if(stackptr->size>=stackptr->maxsize)
        return 1;
    return 0;    
}

int push(Stack* stackptr, Stackdata sdata){
    // copy all of your stack data into stack
    if(isfull(stackptr)){
        return 0;
    }
    int top = stackptr->top;
    stackptr->arr[top].data = sdata.data;
    // copy if you have also another data;
    stackptr->top++;
    stackptr->size++;
    return 1;
}

int pop(Stack* stackptr){
    if(isempty(stackptr))
        return 0;
    stackptr->top--;
    stackptr->size--;
    return 1;
}

Stackdata peek(Stack* stackptr){
    int top = stackptr->top - 1; // also you can check if stack is empty or not
    return stackptr->arr[top]; // or we can return pointer for faster access; (As this will remove additonal copy of elements)
}

void printstack(Stack* stackptr){
    int size = stackptr->size;
    print("Printing Stack");
    for(int i=0;i<size;i++){
        print(stackptr->arr[i].data);
    }
    print("Printing Finished");
}

int main(){
    Stack* ptr;
    Stackdata sdata;
    ptr = getnewstack();
    for(int i=-10;i<399;i++){
        sdata.data=i;
        push(ptr,sdata);
    }
    printstack(ptr);
    pop(ptr);
    pop(ptr);
    sdata = peek(ptr);
    print(sdata.data);

    return 0;
}