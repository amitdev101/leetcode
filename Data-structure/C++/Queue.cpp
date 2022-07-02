#include<iostream>
using namespace std;

#define watch(x) cout<<(#x)<<" is "<<x<<"\n"
#define print(x) cout<<x<<"\n"
#define queuecapacity 100

struct Qdata{
    int mydata; // specify yourdata to be stored in queue 
    // or we can store pointers like Node* nodeptr;
    // Node* ptr;

};

struct Queue{
    Qdata arr[queuecapacity]; // Allocating array of Qdata
    // or we can use a pointer and then allocating the required nodes via malloc in an init func.
    // Qdata *ptr; (ptr = (Qdata*)malloc(sizeof(Qdata)*capacity); )
    int maxsize;
    int size;
    int front;
    int rear;
};

Queue* getnewqueue(){
    Queue* myqueue = (Queue*)malloc(sizeof(Queue));
    myqueue->maxsize = queuecapacity;
    myqueue->size = 0;
    myqueue->front = 0;
    myqueue->rear = 0;
    return myqueue;
}

int getqueuesize(Queue* queueptr){
    return queueptr->size;
}

int isempty(Queue* queueptr){
    if(queueptr->size == 0)
        return 1;
    return 0;           
}

int isfull(Queue* queueptr){
    if(queueptr->size < queueptr->maxsize){
        return 0;
    }
    return 1;
}

int enqueue(Queue* queueptr, Qdata Qdata){
    // set all your Qdata elements into queue
    // here we have taken only mydata of int type 
    // so we copy only this(Qdata.mydata).
    if(isfull(queueptr)){
        print("Queue is full. Cannot add more elements");
        return 0;
    }
    else{
        int maxsize = queueptr->maxsize;
        int rear = queueptr->rear;
        (queueptr->arr)[rear].mydata = Qdata.mydata;
        queueptr->rear = (rear+1)%maxsize;
        queueptr->size++;
        return 1;
    }
}

void dequeue(Queue* queueptr){
    // we will remove the element at front
    if(isempty(queueptr)){
        print("Queue is empty. Cannot dequeue");
    }
    else{
        int front = queueptr->front;
        int maxsize = queueptr->maxsize;
        // print(queueptr->arr[front].mydata);
        front = (front + 1)%maxsize;
        queueptr->front = front;
        queueptr->size--;
    }
}

Qdata peek(Queue* queueptr){
    int front = queueptr->front;
    print(queueptr->arr[front].mydata);
    return (queueptr->arr[front]); // or you can return pointer for faster access;

}

void printqueue(Queue* queueptr){
    int front = queueptr->front;
    int size = queueptr->size;
    int maxsize = queueptr->maxsize;
    for(int i=0;i<size;i++){
        print(queueptr->arr[front].mydata);
        front = (front+1)%maxsize;
    }
}

int main(){
    Queue* myqueueptr;
    myqueueptr = getnewqueue();
    Qdata qdata;
    for(int i=11;i<400;i+=3){
        qdata.mydata = i;
        enqueue(myqueueptr,qdata);
    }
    // printqueue(myqueueptr);
    int size = myqueueptr->size;
    Qdata myqdata;
    for(int i=0;i<size;i++){
        myqdata = peek(myqueueptr);
        dequeue(myqueueptr);
    }
    printqueue(myqueueptr);

    return 0;

}

