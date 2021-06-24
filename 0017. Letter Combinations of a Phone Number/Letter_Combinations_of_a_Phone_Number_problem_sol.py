from typing import List
mydict = {
            2:'abc',
            3:'def',
            4:'ghi',
            5:'jkl',
            6:'mno',
            7:'pqrs',
            8:'tuv',
            9:'wxyz'
        }
anslist = list()

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        global anslist
        anslist = list()
        s=''
        if not digits:
            return anslist
        self.findcomb(digits,s)
        return anslist
    
    def findcomb(self,digits,s):
        if not digits:
            anslist.append(s)
            return
        digit = digits[0]
        tempstr = mydict[int(digit)]
        for char in tempstr:
            self.findcomb(digits[1:],s+char)
    
        
    
        