class Solution:
    def convert(self, st: str, numrows: int) -> str:
        if numrows==1:
            return st
        
        # if numrows are greater than one
        strlist = list()
        for i in range(numrows):
            strlist.append("")
        # we got a list of strings
        # now traverse the list and add the char into string
        dir = 1 # 1 for down, 0 for up direction
        row = 0
        for i in range(len(st)):
            c = st[i]
            strlist[row]+=c
            if row==0:
                dir = 1
            elif row==(numrows-1):
                dir = 0
            
            if dir==1:
                row+=1
            else :
                row-=1
        
        # print(strlist)
        # now add all strings and return it
        ans = ""
        for row in range(numrows):
            ans+=strlist[row]
        return ans
      

def random_testcase_gen():
    import random
    s = "abcdefghijklmnopqrstuvwxyz"
    rows = random.randint(1, 20)
    l = random.randint(1,20)
    randstr = ""
    for i in range(l):
        r = random.randint(0, len(s)-1)
        randstr+=s[r]
    return randstr,rows


if __name__=="__main__":
    for _ in range(100):
        s,r = random_testcase_gen()
        s = "PAYPALISHIRING"
        r = 3

        sol = Solution()
        print(sol.convert(s,r))
        break