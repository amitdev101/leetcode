#include<bits/stdc++.h>
using namespace std;

#define watch(x) cout<<(#x)<<" is "<<x
#define print(x) cout<<x
#define endl cout<<"\n"
class Solution {
public:
    int indexofchar[256]; // to store the index of the traversed char
    int lengthOfLongestSubstring(string s) {
        init();
        int cans=0;
        int ans=0;
        int start = 0;
        int n = s.length();
        for(int i=0;i<n;i++){
            char c = s[i];
            // int index = c - 'a';
            int index = c;
            if(indexofchar[index] == -1 ){ // not visited;
                cans+=1;
            }
            else{
                int lastindex = indexofchar[index];
                if (lastindex < start){ 
                    // if the last index is already behind the start, then it;s new char
                    cans+=1;
                }
                else{
                    cans = i - lastindex;
                    start = lastindex+1;
                }
            }
            if(cans > ans) 
                ans = cans;
            indexofchar[index]=i;

        }
        return ans;

    }


    void init(){
        for(int i=0;i<256;i++){
            indexofchar[i]=-1;
        }
    }

};

int main(){
    print("hello world"); endl;
    Solution mysol;
    // string teststr="abcabc";
    // string teststr="pwwkew";
    string teststr="abba";
    print(teststr.length());
    for(int i=0;i<teststr.length();i++){
        print(teststr[i]);
    }
    endl;
    print(mysol.lengthOfLongestSubstring(teststr));
}