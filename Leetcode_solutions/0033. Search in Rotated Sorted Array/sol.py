from typing import List
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        n = len(nums)
        ans = -1
        lo = 0
        hi = n-1
        
        def search(lo,hi):
            nonlocal ans
            if nums[lo]<=nums[hi] and (nums[hi]<target or target<nums[lo]):
                return
            if nums[lo]<=target<=nums[hi]:
                # means it is a sorted portion
                l,h = lo,hi
                while(l<=h):
                    mid = (l+h)//2
                    if nums[mid]==target:
                        ans = mid
                        return
                    elif nums[mid]<target:
                        l = mid+1
                    else : h = mid-1
            else :
                # means it is not sorted
                mid = (lo+hi)//2
                search(lo,mid)
                search(mid+1,hi)
        
        search(0,n-1)
        return ans
        