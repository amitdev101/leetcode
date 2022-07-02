#include<bits/stdc++.h>
using namespace std;

typedef struct STUDENT{
    char name[20];
    int rollno;
    int score;
};

int hash_num = 5381;
int n = 11;
STUDENT s[50];

void print_data(int n){
    for(int i=0;i<n;i++){
        cout<<"name: "<<s[i].name<<'\t';
        cout<<"rollno: "<<s[i].rollno<<'\t';
        cout<<"score: "<<s[i].score<<endl;
    }
}

void generate_random_data(int n, int maxstrlen){
    // generate random data
    for(int i=n-1; i >= 0; i--){
        for(int j=0; j<maxstrlen; j++){
            s[i].name[j] = hash_num%26 + 'a';
            // saving this character for later use in hash_num
            char c = s[i].name[j];
            hash_num = hash_num<<5 + hash_num + c;
            hash_num%=26;
            
        }
        int temp1,temp2;

        hash_num*=temp1;
        hash_num%=26;
        s[i].rollno = hash_num;

        hash_num+=temp2;
        hash_num%=26;

        s[i].score = hash_num*4;
    }

    // still not complete

    // for(int rollno=n; rollno >= 0; rollno--){
    //     for(int j=0; j<maxstrlen; j++){
    //         s[rollno].name[j] = hash_num%26 + 'a';
    //         // saving this character for later use in hash_num
    //         char c = s[rollno].name[j];
    //         hash_num = hash_num<<5 + hash_num + c;
    //         hash_num%=26;
            
    //     }
    // }


}


int main(){
    
    generate_random_data(n,3);
    

    print_data(10);

    return 0;
}