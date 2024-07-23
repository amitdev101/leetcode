class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class OrderedDict:
    def __init__(self):
        self.dict = {}  # This will store the key to ListNode mapping
        self.head = ListNode(None, None)  # Dummy head
        self.tail = ListNode(None, None)  # Dummy tail
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node):
        """Add node right after head."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node):
        """Remove an existing node from the linked list."""
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def _move_to_head(self, node):
        """Move certain node in between to the head."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self):
        """Pop the current tail."""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key):
        node = self.dict.get(key)
        if not node:
            return None
        # Move the accessed node to the head
        self._move_to_head(node)
        return node.value

    def add(self, key, value):
        node = self.dict.get(key)
        if not node:
            new_node = ListNode(key, value)
            self.dict[key] = new_node
            self._add_node(new_node)
        else:
            # Update the value.
            node.value = value
            self._move_to_head(node)

    def delete(self, key):
        node = self.dict.get(key)
        if node:
            self._remove_node(node)
            del self.dict[key]


if __name__=='__main__':
    # Create the OrderedDict instance
    ordered_dict = OrderedDict()

    # Add elements
    ordered_dict.add("key1", 1)
    ordered_dict.add("key2", 2)
    ordered_dict.add("key3", 3)

    # Retrieve elements
    print(ordered_dict.get("key2"))  # Output: 2
    print(ordered_dict.get("key1"))  # Output: 1

    # Delete an element
    ordered_dict.delete("key2")
    print(ordered_dict.get("key2"))  # Output: None
