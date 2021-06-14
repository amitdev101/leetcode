class Solution:
    def romanToInt(self, s: str) -> int:
        mydict = {
            "I":1,
            "IV":4,
            "V":5,
            "IX":9,
            "X":10,
            "XL":40,
            "L":50,
            "XC":90,
            "C":100,
            "CD":400,
            "D":500,
            "CM":900,
            "M":1000,
        }
        # keylist = list(mydict.keys())
        n = len(s)
        i = 0
        num=0
        while(i<n):
            if i<n-1:
                # ts = s[i:i+2]
                ts = s[i]+s[i+1]
                if ts in mydict:
                    num+=mydict[ts]
                    i+=2
                else:
                    num+=mydict[s[i]]
                    i+=1
                # print(num)
                    
            else:
                num+=mydict[s[i]]
                i+=1
                # print(num)
                
        return num