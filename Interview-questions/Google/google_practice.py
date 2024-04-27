# Q1 https://leetcode.com/problems/my-calendar-i/description/
class Node:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class MyCalendar:

    def __init__(self):
        self.root = Node()

    def book(self, start: int, end: int) -> bool:
        pointer = self.root
        while True:
            if pointer.left is None and pointer.right is None:
                pointer.left = Node(start)
                pointer.right = Node(end)
                return True
            if start >= pointer.right.val:
                pointer = pointer.right
            elif end <= pointer.left.val:
                pointer = pointer.left
            else:
                return False
        


# Your MyCalendar object will be instantiated and called as such:
# obj = MyCalendar()
# param_1 = obj.book(start,end)