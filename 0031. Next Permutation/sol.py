class Solution:
    def nextPermutation(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        i = n-1
        while(i>0):
            if nums[i-1]<nums[i]:
                # find rightmost index which is just greater than nums[i-1]
                j=n-1
                while j>i-1:
                    if nums[j]>nums[i-1]:
                        # jth index found, Now swap it with i-1 index
                        nums[i-1],nums[j] = nums[j], nums[i-1]
                        # now reverse all remaining numbers as these form a descending sorted array , 
                        # so obviously this is the last permutation 
                        # and the next permutation will be the 1st permutiation
                        # reversing array arr = nums[i:]
                        lo = i  #(i-1+1)
                        hi = n-1
                        while (lo <hi):
                            nums[lo],nums[hi] = nums[hi],nums[lo]
                            lo+=1
                            hi-=1
                        return
                    j-=1
            i-=1
    
        for i in range(n//2):
            nums[i],nums[n-1-i] = nums[n-1-i],nums[i]
            
        
            
            
        