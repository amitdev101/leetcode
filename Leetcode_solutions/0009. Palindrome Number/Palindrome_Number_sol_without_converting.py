from typing import List


class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x<0:
            return False
        # solving without converting into str
        # count the digits 
        digitlist = self.get_digit_list(x)
        n = len(digitlist)
        i=0
        j=n-1
        while(i<j):
            if digitlist[i]!=digitlist[j]:
                return False
            i+=1
            j-=1
        return True

    def get_digit_list(self,num: int)->list :
        digitlist = list()
        while(num!=0):
            digitlist.append(num%10)
            num=num//10
        return digitlist

if __name__=='__main__':
    sol = Solution()
    print(sol.isPalindrome(1221))
