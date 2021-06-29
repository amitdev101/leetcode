class Solution:
    def isValid(self, s: str) -> bool:
        c1 = '('
        c2 = '{'
        c3 = '['
        open = c1+c2+c3
        stack = list()
        ans = True
        for c in s:
            if ans==False:
                return ans
            if c in open:
                stack.append(c)
            else :
                if not stack:
                    ans = False
                    return ans

                peek = stack[-1]
                if c==')' and peek!=c1:
                    ans = False
                elif c=='}' and peek!=c2:
                    ans = False
                elif c==']' and peek!=c3:
                    ans = False
                
                stack.pop()
        if stack:
            ans = False
        
        return ans