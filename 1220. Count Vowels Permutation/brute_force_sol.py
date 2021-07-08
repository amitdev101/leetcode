class Solution:
    
    def countVowelPermutation(self, n: int) -> int:
        vowels = ['a','e','i','o','u']
        rule = {
            'a':['e'],
            'e':['a','i'],
            'i':['a','e','o','u'],
            'o':['i','u'],
            'u':['a']
        }
        self.ans = 0
        # @functools.cache
        def permute(s:str=''):
            if len(s)==n:
                self.ans+=1
                return
            if not s:
                for v in vowels:
                    permute(v)
            else :
                c = s[-1]
                chars = rule[c]
                for char in chars:
                    permute(s+char)
            return self.ans%(10**9+7)
        
        return permute()
        
