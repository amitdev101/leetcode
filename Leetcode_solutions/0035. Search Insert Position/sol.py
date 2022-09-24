class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        n = len(nums)
        lo,hi = 0,n-1
        ans = 0
        while(lo<=hi):
            mid=(lo+hi)//2
            if nums[mid]==target:
                return mid
            elif nums[mid]<target:
                lo=mid+1
                ans = lo
            else :
                hi = mid-1
        return ans
        