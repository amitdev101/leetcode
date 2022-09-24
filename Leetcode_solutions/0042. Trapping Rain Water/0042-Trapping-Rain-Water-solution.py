from heapq import *
class Solution:
    def trap(self, height: list[int]) -> int:
        if len(height)<2 :
            return 0
        
        def bruteforce2(height: list[int] = height):
            ans = 0
            n = len(height)
            leftmax = 0
            rightmaxlist = [0 for _ in range(n)]
            rightmaxlist[n-1] = height[n-1]
            for i in range(n-2,-1,-1):
                rightmaxlist[i] = max(height[i],rightmaxlist[i+1])
            for i in range(n):
                leftmax = max(leftmax,height[i])
                rightmax = rightmaxlist[i]
                ans += min(leftmax,rightmax) - height[i]
            return ans
        
        def bruteforce(height: list[int] = height):
            ans = 0
            n = len(height)
            
            for i in range(n):
                leftmax=rightmax=0
                for k in range(i+1):
                    leftmax = max(leftmax,height[k])
                for k in range(i,n):
                    rightmax = max(rightmax,height[k])
                ans += min(leftmax,rightmax) - height[i]
            return ans
        
        def twopointers(height:list = height):
            ans = 0
            lptr, rptr = 0, len(height)-1
            leftmax, rightmax = height[lptr], height[rptr]
            while lptr < rptr:
                if height[lptr] < height[rptr]:
                    leftmax = max(leftmax,height[lptr])
                    ans += leftmax - height[lptr]
                    lptr+=1
                else :
                    rightmax = max(rightmax, height[rptr])
                    ans+= (rightmax - height[rptr])
                    rptr-=1
            return ans
                    
        return twopointers()
    