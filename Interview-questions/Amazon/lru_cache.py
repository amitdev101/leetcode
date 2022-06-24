class Node:
    def __init__(self,key,value,prev=None,next=None):
        self.key = key
        self.value = value
        self.prev = prev
        self.next = next

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.dict = dict()
        
        self.dummyhead = Node(-1,-1)
        self.dummytail = Node(-1,-1)
        self.dummyhead.next = self.dummytail
        self.dummytail.prev = self.dummyhead
    
    def movetofront(self,node):
        # delete from middle and move it to end of dll
        prevnode = node.prev
        nextnode = node.next
        prevnode.next = nextnode
        nextnode.prev = prevnode
         # last node 
        lastnode = self.dummytail.prev
        lastnode.next = node
        node.prev = lastnode
        node.next = self.dummytail
        self.dummytail.prev = node
    
    # def printll(self):
    #     node = self.dummyhead.next
    #     while node :
    #         print(f"({node.key},{node.value})->",end="")
    #         node = node.next
    #     print("None")
        
    
    def get(self, key: int) -> int:
        if key in self.dict:
            # move this key to front
            node = self.dict[key]
            self.movetofront(node)
            return node.value
        else : return -1

    def put(self, key: int, value: int) -> None:
        if key in self.dict:
            node = self.dict[key]
            self.movetofront(node)
            # updating values
            node.value = value
        else :
            node = Node(key,value)
            lastnode = self.dummytail.prev
            lastnode.next = node
            node.prev = lastnode
            node.next = self.dummytail
            self.dummytail.prev = node
            
            # add this key 
            self.dict[key] = node
            
        size = len(self.dict.keys())
        
        if (size>self.capacity):
            firstnode = self.dummyhead.next
            secondnode = firstnode.next
            self.dummyhead.next = secondnode
            secondnode.prev = self.dummyhead
            
            # deleting key and node
            self.dict.pop(firstnode.key,None)
            del firstnode
            
            
            
                
            
            
            


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)