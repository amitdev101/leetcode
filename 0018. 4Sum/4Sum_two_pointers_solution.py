from typing import List
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        ansset = set()
        n = len(nums)
        for i in range(n):
            if i>3 and nums[i]==nums[i-3]: # in case all four numbers are same. skip it
                continue
            for j in range(i+1,n):
                lo = j+1
                hi = n-1
                num = target - (nums[i]+nums[j])
                # select last two numbers via two pointer method
                while(lo<hi):
                    newsum = nums[lo] + nums[hi]
                    if newsum==num:
                        templist = [nums[i],nums[j],nums[lo],nums[hi]]
                        ansset.add(tuple(templist))
                        lo+=1
                        hi-=1
                    elif newsum<num:
                        lo+=1
                    else :
                        hi-=1
        return ansset