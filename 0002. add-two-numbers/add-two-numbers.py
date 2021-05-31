# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        #  reverse ll 
        l1 = self.reversell(l1)
        l2 = self.reversell(l2)
        num1 = self.computell(l1)
        num2 = self.computell(l2)
        # num1 = int(str(num1)[::-1])
        # num2 = int(str(num2)[::-1])
        num = num1+num2
        print(num1,num2,num)
        return self.returnll(num)
        
    def computell(self,l1):
        num = 0
        temp = 0
        while(l1!=None):
            temp = l1.val
            num = num*10 + temp;
            l1 = l1.next
        return num
    
    def returnll(self,num):
        if num == 0:
            return ListNode(num)
        tail = None
        head = None
        while(num!=0):
            r = num%10
            num//=10
            tempnode = ListNode(r)
            if(tail):
                tail.next = tempnode
                tail = tail.next
            else :
                head = tempnode
                tail = tempnode
        return head
           
    def reversell(self,ll: ListNode):
        head = None
        tail = None
        # reversing a ll 
        temp = True
        while(ll!=None):
            temp = ll.val
            tempnode = ListNode(temp)
            if(head):
                # insert at head
                temp.next = head
                head.next = temp
            else :
                # initialize head and tail
                head = tempnode
                tail = tempnode
        return head

        