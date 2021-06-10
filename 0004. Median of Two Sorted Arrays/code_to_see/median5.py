class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        lens = len(nums1) + len(nums2)
        if lens % 2 == 1:
            return self.kthSmallest(nums1, nums2, lens//2)
        else:
            return ( self.kthSmallest(nums1, nums2, lens//2 - 1) + self.kthSmallest(nums1, nums2, lens//2) ) / 2.0
        
    def kthSmallest(self, nums1, nums2, k):
        if not nums1:
            return nums2[k]
        if not nums2:
            return nums1[k]
        
        midIdx1, midIdx2 = len(nums1)//2, len(nums2)//2
        midVal1, midVal2 = nums1[midIdx1], nums2[midIdx2]
        
        # when k is relatively large, then we can safely drop the first half that are surely smaller than the kth
        # the question is where is the first half that are surely smaller than the kth?
        # by comparing midVal1 and midVal2, we can find it out
        # if midVal1 < midVal2, then all the vals in nums1[:midIdx1] are less than midVal2 
        # also all of those vals are less than kth, we can safely drop all those vals
        if k > midIdx1 + midIdx2:
            if midVal1 < midVal2:   
                return self.kthSmallest(nums1[midIdx1 + 1:], nums2, k - midIdx1 - 1)
            else:
                return self.kthSmallest(nums1, nums2[midIdx2 + 1:], k - midIdx2 - 1)
            
        # when k is relatively small, then we can safely drop the second half that are surely larger than the kth
        # the question is where is the second half that are surely larger then the kth?
        # by comparing midVal1 and midVal2, we can find it out
        # if midVal1 > midVal2, then all the vals in nums1[midIdx1:] are larger than midVal2
        # also all of those vals are larger than kth, we can safely drop all those vals
        else:
            if midVal1 > midVal2:
                return self.kthSmallest(nums1[:midIdx1], nums2, k)
            else:
                return self.kthSmallest(nums1, nums2[:midIdx2], k)