class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        n = len(nums)
        arr = [True for i in range(n+2)]
        arr[0] = False
        
        for num in nums:
            if 0<num<=(n+1):
                arr[num]=False
        for i in range(n+2):
            if arr[i]==True:
                return i
            
        