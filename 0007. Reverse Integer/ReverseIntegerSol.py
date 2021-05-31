class Solution:
    b = pow(2,31) - 1
    a = -pow(2,31)
    def reverse(self, x: int) -> int:
        num = x
        negative = 0
        if num<0:
            negative = 1
            num = -num
        rnum = 0
        while(num!=0):
            r = num%10
            num = num//10
            rnum = rnum*10 + r
        if negative:
            rnum= -rnum
        a = Solution.a
        b = Solution.b
        if a<=rnum<=b:
            return rnum
        else : return 0

if __name__=="__main__":
    num = -123
    sol = Solution()
    print(sol.reverse(num))
