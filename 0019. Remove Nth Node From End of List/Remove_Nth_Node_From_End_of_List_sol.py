from typing import List
# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        pcrawl = head
        l = 0
        while(pcrawl):
            l+=1
            pcrawl=pcrawl.next
        
        # nth node from last , then the index will be s = (l+1) - n
        s = l+1-n
        i = 0
        pcrawl = head
        if s==0:
            head = head.next

        else:
            while(pcrawl):
                i+=1
                if i==(s-1):
                    prev = pcrawl
                elif i==s+1 and i<=l:
                    next = pcrawl
                pcrawl=pcrawl.next
            
            prev.next = next
            pcrawl = pcrawl.next
        