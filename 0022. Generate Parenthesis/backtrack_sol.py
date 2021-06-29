
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        ans = list()
        def backtrack(s:list=list(), l:int=0, r:int=0):
            if len(s)==2*n:
                ans.append("".join(s))
                return
            if l<n:
                s.append('(')
                backtrack(s,l+1,r)
                s.pop()
                
            if r<l:
                s.append(')')
                backtrack(s,l,r+1)
                s.pop()
                
        backtrack()
        return ans
                
                
            
            
            
        