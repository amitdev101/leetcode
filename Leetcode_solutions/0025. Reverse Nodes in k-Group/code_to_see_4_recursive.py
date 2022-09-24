# https://leetcode.com/problems/reverse-nodes-in-k-group/discuss/1297018/Python-solution-using-recursion-(faster-than-90-of-the-submissions)
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):

    # returns the length of the passed linked list
    def lengthList(self, head):
        temp = head
        count = 0
        while temp != None:
            count += 1
            temp = temp.next
        return count
		
	# returns the head and tail of the passed linked list after reversing it
    def reverseList(self, head):
        if head == None or head.next == None:
            return [head, head]
        temp = head.next
        head.next = None
        [tempHead, tempTail] = self.reverseList(temp)
        tempTail.next = head
        tempTail = head
        return [tempHead, tempTail]
	
	# reverses a given linked list in groups of k and returns its head and tail
    def reverseGroup(self, head, k):
        lengthOfList = self.lengthList(head)
        if lengthOfList < k:
            return [head, head]
        temp = head
        for i in range(k):
            temp1 = temp
            temp = temp.next
        temp1.next = None
        [tempHead, tempTail] = self.reverseGroup(temp, k)
        [temp1Head, temp1Tail] = self.reverseList(head)
        if tempHead == None:
            return [temp1Head, temp1Tail]
        else:
            temp1Tail.next = tempHead
            return [temp1Head, tempTail]
        return [None, None]
		
	# return the head of the passed linked list after reversing it in groups of k
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        return self.reverseGroup(head, k)[0]