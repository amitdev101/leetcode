class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        if n==0:
            return ""
        longest_palindrome = ""
        for midpos in range(n):
            newstr1 = self.calc_palindrome(s,midpos,midpos)
            newstr2 = self.calc_palindrome(s,midpos,midpos+1)
            longest_palindrome = max([longest_palindrome, newstr1, newstr2], key=lambda x : len(x))
        
        return longest_palindrome
    
    def calc_palindrome(self,s,i,j):
        l = i
        r = j
        move = 0
        while(l>=0 and r<=(len(s)-1) and s[l]==s[r]):
            move+=1
            l-=1
            r+=1
        # valid string is from (l+1,r-1)
        return s[l+1:r]
                



if __name__=="__main__":
    teststr = "abadd"
    # teststr = "aaabb"
    sol = Solution()
    print(sol.longestPalindrome(teststr))
