class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        if self.mymatch(0,s,0,p):
            return True
        return False
    
    def mymatch(self,i,s,j,p):
        sn = len(s)
        pn = len(p)
        if j==pn:
            return i==sn
#       case 1 if next is *
        if j+1<pn and p[j+1]=='*' :
            if self.mymatch(i,s,j+2,p):
                return True
            while (i<sn and (s[i]==p[j] or p[j]=='.')):
                if self.mymatch(i+1,s,j+2,p):
                    return True
                i+=1
        elif i<sn and (s[i]==p[j] or p[j]=='.') :
            if self.mymatch(i+1,s,j+1,p):
                  return True
        
        else : return False
        
        
        