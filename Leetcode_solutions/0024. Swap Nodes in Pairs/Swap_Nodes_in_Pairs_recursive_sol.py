# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        dummy = ListNode(0)
        dummy.next = head
        
        def reverse(head):
            if not head:
                return
            if head and not head.next:
                return head
            newhead = head.next
            headtoreverse = head.next.next
            head.next.next = head
            head.next = reverse(headtoreverse)
            
            return newhead
        
        return reverse(head)
            
            
            
        