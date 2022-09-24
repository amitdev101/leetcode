from heapq import *
from typing import List
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        h = [] # use min heap with size k
        for n in nums[:k]:
            heappush(h, n)
        for n in nums[k:]:
            if n > h[0]:
                heapreplace(h, n)
        return heappop(h)