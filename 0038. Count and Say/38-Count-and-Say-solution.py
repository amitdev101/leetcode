class Solution:
    def countAndSay(self, n: int) -> str:
        def countnum(n: int):
            if n<=1:
                return "1"
            else :
                num = countnum(n-1)
                newnum = countdigits(num)
                return newnum
        
        def countdigits(num : str):
            
            n = len(num)
            count = 1
            ans = ""
            if n==1:
                ans+=("1"+num[0])
                return ans
            
            for i in range(n-1):
                if num[i]==num[i+1]:
                    count+=1
                else :
                    ans+= (str(count)+num[i])
                    count=1
                    
            ans+=(str(count)+num[-1])
            return ans
        
        return countnum(n)
            
                    
                
                
                
        