#include<iostream>
#include<malloc.h>
using namespace std;

#define capacity 113

int djbhash(char str[]){
    int hash = 5381;
    for(int i=0;str[i]!='\0';i++){
        hash = (hash<<5) + hash + str[i]; // hash = hash*33 + str[i]
        if(hash>=capacity){
            hash = hash%capacity;
        }
    }
    return hash;
}

typedef struct HASHNODE{
    char key[100];
    int value;
    struct HASHNODE* next;
};

HASHNODE* hashtable[capacity];

void mystrcpy(char dest[],char src[]){
    int i=0;
    while(src[i]!='\0'){
        dest[i]=src[i];
        i++;
    }
    dest[i]='\0';
}

bool mycmp(char s1[],char s2[]){
    // return true if both strings are equal
    int i;
    for(i=0;s1[i]!='\0';i++){
        if(s2[i]!='\0'|| s1[i]!=s2[i])
            return false;
    }
    if(s2[i]=='\0')
        return true;
    return false;
}


HASHNODE* gethashnode(char key[],int value){
    HASHNODE* temp = (HASHNODE*)malloc(sizeof(HASHNODE));
    mystrcpy(temp->key,key);
    temp->value = value;
    temp->next =   NULL;
    return temp;
}

void inithashtable(){
    for(int i=0;i<capacity;i++){
        hashtable[i]=NULL;
    }
}

void insertkey(char key[],int value){
    int index = djbhash(key);
    HASHNODE* t = gethashnode(key,value);
    t->next = hashtable[index];
    hashtable[index]=t;
}

int getvalue(char key[]){
    int index = djbhash(key);
    HASHNODE* crawlptr = hashtable[index];
    while(crawlptr){
        if(mycmp(crawlptr->key,key)){
            return crawlptr->value;
        }
        crawlptr = crawlptr->next;
    }
    return -1; // indicates value not present;
}

void deletekey(char key[]);

int main(){
    return 0;
}