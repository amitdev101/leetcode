from typing import List
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        first,last = -1,-1
        if not nums:
            return [-1,-1]
        if len(nums)==1:
            if target==nums[0]:
                return [0,0]
            else : return [-1,-1]
        
        def search(lo,hi):
            nonlocal first,last
            
            if 0<=lo<=hi<len(nums) and nums[lo]<=target<=nums[hi]:
                mid = (lo+hi)//2
                if nums[mid]==target:
                    if first==-1:
                        first = mid
                    else : first = min(first,mid)
                    last = max(last,mid)
                if (mid-1)!=hi: # prevent infinite recursion
                    search(lo,mid-1)
                if lo!=(mid+1): # prevent infinite recursion
                    search(mid+1,hi)
                
        search(0,len(nums)-1)
        return [first,last]
            
            