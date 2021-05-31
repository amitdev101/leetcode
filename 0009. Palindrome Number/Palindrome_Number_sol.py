class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x<0:
            return False
        # solving with converting into str
        s = str(x)
        n = len(s)
        i=0
        j=n-1
        while(i<j):
            if s[i]!=s[j]:
                return False
            i+=1
            j-=1
        return True

if __name__=='__main__':
    sol = Solution()
    print(sol.isPalindrome(-1221))
