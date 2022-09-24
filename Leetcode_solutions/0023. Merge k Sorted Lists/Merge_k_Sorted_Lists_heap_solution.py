from typing import List
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
# from queue import PriorityQueue
from heapq import *
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        c = 0
        head = point = ListNode(0)
        q = list()
        for l in lists:
            if l:
                heappush(q,(l.val,c,l)) # priority, index/counter, item
                # index/counter is also pushed so that we can break tie ups between two nodes with same values.
                c+=1
        
        while len(q)>0:
            val,c,node = heappop(q)
            point.next = ListNode(val)
            point = point.next
            node = node.next
            if node:
                heappush(q,(node.val,c,node))
                c+=1
        return head.next
            
            

            
        