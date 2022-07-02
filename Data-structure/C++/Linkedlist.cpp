#include<iostream>
using namespace std;
#define watch(x) cout<<(#x)<<" is "<<x<<"\n"
#define print(x) cout<<x<<"\n"

// linked list 

// creating a struct for singly linked list
struct Node{
    int data;
    Node *next;
};

Node* getnewnode(){
    Node *temp = (Node*)malloc(sizeof(Node));
    temp->data = -1;
    temp->next = NULL;
    return temp;
}


int main(){
    return 0;
}






// ############# Extra code to test #############
struct Nodevec{
    struct Node arr[100];
    int size;
};

Nodevec* create_node_vec(int arr[],int n){
    Nodevec* temp = (Nodevec*)malloc(sizeof(Nodevec));
    temp->size = 0;
    for(int i=0;i<n;i++){
        int num = arr[i];
        Node* nodeptr = getnewnode();
        nodeptr->data = num;
        // not linking now the next ptr
        temp->arr[temp->size++] = *nodeptr;

    }
    for(int i=0;i<n-1;i++){
        temp->arr[i].next = &(temp->arr[i+1]);
    }

}

