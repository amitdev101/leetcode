#include<bits/stdc++.h>
using namespace std;
#define watch(x) cout<<(#x)<<" is "<<x
class Solution {
public:
    string convert(string s, int numrows) {
        if(numrows==1)
            return s;
        vector<string> strlist;
        for(int i=0;i<numrows;i++){
            strlist.push_back("");
        }
        // watch(strlist);
        
        int n = s.length();
        int dir = 1; //for down else up
        int r = 0;
        for(int i=0;i<n;i++){
            strlist[r]+=s[i];
            if(r==0)
                dir = 1;
            else if (r==numrows-1)
                dir = 0;
            if(dir)
                r+=1;
            else 
                r-=1;
        }
        string ansstr="";
        for(int i=0;i<numrows;i++){
            ansstr+=strlist[i];
        }
        return ansstr;
    }
};