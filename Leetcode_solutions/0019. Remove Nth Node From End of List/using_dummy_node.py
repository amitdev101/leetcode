def removeNthFromEnd(self, head, n):
    dummy = l = ListNode(0)
    dummy.next = r = head
    for _ in range(n):
        r = r.next
    while r:
        l, r = l.next, r.next
    l.next = l.next.next
    return dummy.next
    