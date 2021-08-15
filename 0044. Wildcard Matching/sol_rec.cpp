#include<bits/stdc++.h>
using namespace std;
#define watch(x) cout<<(#x)<<" = "<<x<<endl;
class Solution {
public:
    Solution(){
        cout<<"calling constructor\n";
    }
    bool isMatch(string s, string p) {
        return ismatch(s,p);
        
    }
    bool ismatch(string s,string p, int i=0, int j=0){
        int sn = s.size();
        int pn = p.size();
        // base case
        if ((i==sn) && (j==pn)){
            return true;
        }
        else if (i>sn  || j>pn){
            return false;
        }
        else {
            char pc = p[j];
            char sc = s[i];
            if(pc=='?'){
                return ismatch(s,p,i+1,j+1);
            }
            else if (pc=='*'){
                for(int k=i;k<=sn;k++){
                    if(ismatch(s,p,k,j+1)){
                        return true;
                    }
                }
            }
            if (sc==pc){
                return ismatch(s,p,i+1,j+1);
            }
        }
        return false;


    }
};

int main(){
    Solution mysol;
    string s = "Hello";
    string p = "Pello";
    bool ans = mysol.isMatch(s,p);
    watch(ans);
    return 0;

}