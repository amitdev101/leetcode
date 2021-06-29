# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution:
    def swapPairs(self, head: ListNode) -> ListNode:
        dummy = ListNode(0)
        dummy.next = head
        pcrawl = head
        if not head or not head.next : return
        head = dummy
        while pcrawl:
            if pcrawl and pcrawl.next:
                newhead = pcrawl.next
                newpcrawl = pcrawl.next.next
                pcrawl.next.next = pcrawl
                head.next = pcrawl.next
                
                
                # change pcrawl
                pcrawl = newpcrawl
                head = newhead
                
        
        return dummy.next
                
            
if __name__=='__main__':
    sol = Solution()
    import random
    numbers = [random.randint(0,10) for i in range(4)]
    head = ListNode(numbers[0])
    pcrawl = head
    for number in numbers[1:]:
        node = ListNode(number)
        pcrawl.next = node
    sol.swapPairs(head)

            
            
            
        