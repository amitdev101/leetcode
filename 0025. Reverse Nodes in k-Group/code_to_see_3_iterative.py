# https://leetcode.com/problems/reverse-nodes-in-k-group/discuss/1297120/Python%3A-O(n)-time-O(1)-space-without-recursion
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def listLength(self, head):
        temp = head
        count = 0
        while temp != None:
            count += 1
            temp = temp.next
        return count
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        list_length = self.listLength(head)
        if list_length == 1 or k == 1 or list_length < k:
            return head
        reverses = list_length//k
        remainders = list_length%k
        dummy = ListNode()
        previousHead = dummy
        previousTail = None
        temp = head
        while reverses > 0:
            tempHead = temp
            for i in range(k):
                temp1 = temp.next
                temp.next = previousTail
                previousTail = temp
                temp = temp1
            previousHead.next = previousTail
            previousTail = None
            previousHead = tempHead
            reverses -= 1
        if remainders > 0:
            previousHead.next = temp
        return dummy.next
