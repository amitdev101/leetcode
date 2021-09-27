#include<bits/stdc++.h>
using namespace std;
#define watch(x) cout<<(#x)<<" = "<<x<<endl;
int dp[2001][2001];
class Solution {
private:
    
public:
    // Solution(int a){
    //     cout<<"calling constructor\n";
    // }
    bool isMatch(string s, string p) {
        int sn = 2000;
        int pn = 2000;
        for(int i=0;i<=sn;i++){
            for(int j=0;j<=pn;j++){
                dp[i][j]=-1;
            }
        }
        // int sn = s.size(), pn = p.size();
        // dp[sn][pn] = 1;
        return ismatch(s,p);
        
    }
    bool ismatch(string s,string p, int i=0, int j=0){
        if(dp[i][j]!=-1){
            return dp[i][j];
        }
        int sn = s.size();
        int pn = p.size();
        // base case
        if ((i==sn) && (j==pn)){
            dp[i][j]=1;
            return dp[i][j];
        }
        else {
            char pc = p[j];
            char sc = s[i];
            if(pc=='?'){
                dp[i][j] = ismatch(s,p,i+1,j+1);
                return dp[i][j];
            }
            else if (pc=='*'){
                for(int k=i;k<=sn;k++){
                    if(ismatch(s,p,k,j+1)){
                        dp[i][j] = 1;
                        return dp[i][j];
                    }
                    
                }
            }
            if (sc==pc){
                dp[i][j] = ismatch(s,p,i+1,j+1);
                return dp[i][j];
            }
        }
        dp[i][j]=0;
        return false;


    }
};

int main(){
    cout<<"in main\n";
    Solution mysol;
    // string s = "Hello";
    string s = "fg";
    string p = "???";
    int ans = mysol.isMatch(s,p);
    watch(ans);
    return 0;

}
