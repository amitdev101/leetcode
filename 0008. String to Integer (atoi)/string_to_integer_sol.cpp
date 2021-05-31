#define ll long long 
#include<math.h>
class Solution {
public:
    ll int l1 = -pow(2,31);
    ll int l2 = pow(2,31) - 1;
    int myAtoi(string s) {
        ll int num=0;
        ll int actualnum=num;
        int n=s.length();
        bool negative=false;
        // remove white space and for the first character
        int i=0;
        while(s[i]==' '){
            i++;
        }
        // from here i recieve a char that is not space
        char c = s[i];
        if(c=='+' || c=='-'){
            if(c=='-'){
                negative=true;
            }
            i++;
        }
        
        for(;i<n;i++){
            c=s[i];
            int numc = c-'0';
            if(numc>=0 && numc<=9){
                num=num*10+numc;
                // checking the number
                actualnum = num;
                if(negative){
                    actualnum = -actualnum;
                }
                if(actualnum<l1){
                    return l1;
                }
                if (actualnum>l2){
                    return l2;
                }
            }
            else{
                break;
            }
            
        }
        return actualnum;
        
    }
};