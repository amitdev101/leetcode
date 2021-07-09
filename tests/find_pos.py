class Solution:
    def searchRange(self, nums: list[int], target: int) -> list[int]:
        first,last = -1,-1
        
        def search(lo,hi):
            nonlocal first,last
            if nums[lo]<=target<=nums[hi]:
                mid = (lo+hi)//2
                if nums[mid]==target:
                    if first==-1:
                        first = mid
                    else : first = min(first,mid)
                    last = max(last,mid)
                if lo!=hi:
                    search(lo,mid-1)
                    search(mid+1,hi)
                
        search(0,len(nums)-1)
        return [first,last]
            
if __name__=="__main__":
    sol = Solution()
    nums = [5,7,7,8,8,10]
    target = 8
    print(sol.searchRange(nums,target))