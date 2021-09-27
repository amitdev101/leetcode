class Solution:
    def divide(self, dividend: int, divisor: int) -> int:
        positive = (dividend<0) == (divisor<0)
        # print(positive, False==False)
        divd = abs(dividend)
        divs = abs(divisor)
        q = 0
        while(divd>=divs):
            temp,i = divs,1
            while(divd>=temp):
                divd-=temp
                q+=i
                temp=temp<<2
                i = i<<2
        if not positive :
            q=-q
        maxr = 2**31
        if -maxr<=q<=maxr-1:
            return q
        else: return maxr-1 