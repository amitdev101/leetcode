class Solution:
    def longestValidParentheses(self, s: str) -> int:
        maxans = 0
        stack = list()
        stack.append(-1) ## to handle 0th element
        for i in range(len(s)):
            c = s[i]
            if c=='(':
                stack.append(i)
            else :
                x = stack.pop()
                # check whether stack is empty or not 
                if not stack: 
                    stack.append(i)
                else :
                    maxans = max(maxans,i-stack[-1])
                    
        return maxans