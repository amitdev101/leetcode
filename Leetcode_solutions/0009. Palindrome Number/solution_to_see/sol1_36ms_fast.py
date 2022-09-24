class Solution:
    def isPalindrome(self, x: int) -> bool:
        L = 2**31
        MAX = L-1
        MIN = -L
        if not MIN < x < MAX :
            return False
            
        if x <0 :
            return False
        
        x = str(x)
        rev_x = x[::-1]
        if int(rev_x) > L:
            return False 
        
        if x == rev_x :
            return True
        else:
            return False

## logic ##
''' comparing int is faster
use built int str() and int() function :
reverse the string and convert it to int
and check where num and reverse num is same or not
'''