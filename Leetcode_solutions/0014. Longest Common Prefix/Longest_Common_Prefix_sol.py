List = list
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        n = len(strs)
        prefix = strs[0]
        for i in range(1,n):
            prefix = self.findprefix(prefix,strs[i])
        return prefix
    
    def findprefix(self,s,t):
        ans = ''
        for i,v in zip(s,t):
            if i==v:
                ans+=i
            else : break
        return ans