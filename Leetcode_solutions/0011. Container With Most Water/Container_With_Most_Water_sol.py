class Solution:
    def maxArea(self, height: list[int]) -> int:
        ans = 0
        n = len(height)
        lptr = 0
        rptr = n-1
        while(lptr<rptr):
            container = (rptr-lptr)*min(height[lptr],height[rptr])
            if container > ans:
                ans = container
            if height[lptr] < height[rptr]:
                lptr+=1
            else :
                rptr-=1
        return ans
        