from typing import List
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        ans = float('inf')
        nums.sort()
        n = len(nums)
        for i in range(n):
            lo = i+1
            hi = n-1
            while(lo<hi):
                sum = nums[lo] + nums[hi] + nums[i]
                if sum==target :
                    return target
                elif sum<target:
                    lo+=1
                else :
                    hi-=1
                
                if abs(sum-target) < abs(ans-target):
                    ans = sum
                    
        return ans
                
                
                
                    
        
        