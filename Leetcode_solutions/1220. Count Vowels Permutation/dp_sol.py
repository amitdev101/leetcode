class Solution:
    
    def countVowelPermutation(self, n: int) -> int:
        vowels = ['a','e','i','o','u']
        def dpsol():
            mod = 10**9+7
            vm = dict() # vowel map for converting char into index
            for i in range(len(vowels)):
                vowel = vowels[i]
                vm[vowel] = i

            templist = [0 for i in range(n+1)]
            dp = list()
            dp = [templist[:] for vowel in vowels] # creating a deep copy
            # dp[char][n] = dp[5][n]
            # Base case
            # when n = 1. the ans = 1 
            for vowel in vowels:
                dp[vm[vowel]][1] = 1
            # now solve dp for rest of the cases
            for i in range(2,n+1):
                 # case a
                dp[0][i] = dp[1][i-1]
                # case e 
                dp[1][i] = (dp[0][i-1] + dp[2][i-1])%mod
                # case i
                dp[2][i] = (dp[0][i-1] + dp[1][i-1] + dp[3][i-1] + dp[4][i-1])%mod
                # case o
                dp[3][i] = (dp[2][i-1] + dp[4][i-1])%mod
                # case u
                dp[4][i] = dp[0][i-1]
                
            ans = 0
            for i in range(5):
                ans+=dp[i][n]
                ans%=mod
            return ans
                
        return dpsol()
                
                
                
        
            
        
                    
        