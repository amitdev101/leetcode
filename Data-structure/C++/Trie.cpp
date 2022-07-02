#include<iostream>
using namespace std;
#include<malloc.h>

struct trienode{
    struct trienode *child[26];
    int count; // for counting duplicate strings
};

struct trienode mempool[100005];
int memsize=0;

trienode* mymalloc(){
    if(memsize<100005){
        return &mempool[memsize++];
    }
    else{
        trienode* tempnode = (trienode*)malloc(sizeof(trienode));
        return tempnode;
    }
}

trienode* getnewnode(){
    trienode* temp = mymalloc();
    for(int i=0;i<26;i++){
        temp->child[i]=NULL;
    }
    temp->count = 0;
}

struct trienode* root; // defined globally (always try to pass a copy in a function)

void init_trie(){
    memsize=0;
    root = getnewnode();

}

void trie_insert(const char *key){
    // key is a string 
    trienode* pcrawl = root;
    int index,i=0;
    while(key[i]!='\0'){
        index = key[i]-'a';
        if(pcrawl->child[index]==NULL){
            pcrawl->child[index]=getnewnode();
        }
        pcrawl = pcrawl->child[index];
        i++;
    }
    //insertion is complete now increase the count
    pcrawl->count++;
}

bool trie_search(const char *key){
    trienode* pcrawl = root;
    int index,i=0;
    while(key[i]!='\0'){
        index = key[i];
        if(pcrawl->child[index]){// sometimes root doesn't exist so check whether root is null or not;
            return false;
        }
        pcrawl = pcrawl->child[index];
        i++;
    }
    if(pcrawl->count>0){
        return true;
    }
    return false;
}

void trie_delete(const char *key){
    trienode* pcrawl = root;
    if(pcrawl==NULL){
        return;
    }
    int index,i=0;
    while(key[i]!='\0'){
        index = key[i]-'a';
        if(pcrawl->child[index]==NULL){
            return;
        }
        pcrawl = pcrawl->child[index];
        i++;
    }

    if(pcrawl->count > 0){//sometimes key prefix is given and you dont have to delete it; he from hello string
        pcrawl->count--;
    }
}

void crawl_trie( trienode * r){
    if(r==NULL)
        return;
    for(int i=0;i<26;i++){
        if(r->child[i]){
            crawl_trie(r->child[i]);
        }
    }
}

