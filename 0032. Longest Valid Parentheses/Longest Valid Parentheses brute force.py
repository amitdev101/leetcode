class Solution:
    def longestValidParentheses(self, s: str) -> int:
        ans = 0
        n = len(s)
        for i in range(n):
            for j in range(i+1,n):
                if self.isvalid(s[i:j+1]):
                    ans = max(ans,(j-i+1))
        return ans
        
    def isvalid(self,s:str):
        ans = 0
        count = 0
        for c in s:
            if c=='(':
                count+=1
            else : count-=1
            if count<0:
                return 0
            
        if count==0:
            return 1
        else :
            return 0
                
