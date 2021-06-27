from typing import List
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        ansset = set()
        numbervisitedset = set() # to store number previous than index i
        n = len(nums)
        for i in range(n):
            if i>3 and nums[i]==nums[i-3]: # in case of repeated nums and removing computations
                continue
            for j in range(i+1,n):
                for k in range(j+1,n):
                    num = target - (nums[i]+nums[j]+nums[k])
                    if num in numbervisitedset:
                        ansset.add((nums[i],nums[j],nums[k],num))
            numbervisitedset.add(nums[i])
            
        return ansset
        