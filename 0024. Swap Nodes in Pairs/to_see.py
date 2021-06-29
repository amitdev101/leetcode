# https://leetcode.com/problems/swap-nodes-in-pairs/discuss/1305260/20-ms-python3-solution-beats-99-very-straightforward

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
def swapPairs(self, head: ListNode) -> ListNode:
    if not head or not head.next: return head    
    d=l=ListNode()
    while head and head.next:
        d.next=head.next
        head.next=head.next.next
        d.next.next=head
        d=d.next.next
        head=head.next
    return l.next
