# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1:
            return l2
        if not l2:
            return l1
        dhead = ListNode(-1)
        pcrawl = dhead
        while(l1 and l2):
            if l1.val < l2.val:
                pcrawl.next = l1
                l1 = l1.next
            else :
                pcrawl.next = l2
                l2 = l2.next  
            pcrawl = pcrawl.next
                
        if l1 :
            pcrawl.next = l1
        elif l2 :
            pcrawl.next = l2
            
                
        return dhead.next
                    
