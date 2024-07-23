'''
Understanding Segment Trees
What is a Segment Tree?

A Segment Tree is a binary tree used for storing intervals or segments. It allows querying which of the stored segments contain a given point, or querying for all segments overlapping a given segment efficiently.

Segment trees are particularly useful when dealing with static or dynamic ranges of data, where you need to perform multiple range queries and updates efficiently.
Why Use Segment Trees?

Segment trees are used to solve problems that involve frequent range queries and updates on an array or a range of data. Examples include:

    Range sum queries
    Range minimum/maximum queries
    Range frequency queries
    Dynamic interval management (like the problem at hand)

Identifying Problems Solvable by Segment Trees

A problem can typically be solved by a segment tree if it involves:

    Range Queries: Queries that ask for information about a range of elements.
    Range Updates: Updates that modify a range of elements.

In our specific problem, we need to efficiently manage intervals (range updates) and count the number of unique integers covered by these intervals (range queries).
Segment Tree Structure

A segment tree for an array of size n is a binary tree with 2n - 1 nodes. Each node represents an interval [start, end]. The root node represents the entire range [1, n]. Each internal node represents the union of the intervals of its children.
Node Structure

Each node stores:

    The range it represents (start, end).
    Information about the range (like sum, min, max, etc., depending on the problem).
    Lazy propagation values (for range updates).

Building a Segment Tree

To build a segment tree:

    Initialize Nodes: Start with the root representing the whole range.
    Recursively Split: Split the range into two halves and initialize the child nodes.
    Merge Results: Use the results of child nodes to initialize the current node.

Operations on Segment Trees
Update Operation

    Propagate Lazy Values: Before making any updates, ensure all lazy updates are applied.
    Update Range: Update the current node if it falls within the update range. If not, recursively update the child nodes.
    Merge Results: After updating child nodes, merge their results to update the current node.

Query Operation

    Propagate Lazy Values: Ensure all lazy updates are applied before querying.
    Query Range: If the current node's range is completely within the query range, return its value. If not, recursively query the child nodes.
    Merge Results: Merge the results of child nodes to get the query result.

Implementing a Segment Tree with Lazy Propagation

Here is a detailed Python implementation:

python
'''
class SegmentTree:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (4 * n)
        self.lazy = [0] * (4 * n)

    def _update_range(self, node, start, end, l, r):
        if self.lazy[node] != 0:
            self.tree[node] = (end - start + 1)
            if start != end:
                self.lazy[node * 2] = 1
                self.lazy[node * 2 + 1] = 1
            self.lazy[node] = 0

        if start > end or start > r or end < l:
            return

        if start >= l and end <= r:
            self.tree[node] = (end - start + 1)
            if start != end:
                self.lazy[node * 2] = 1
                self.lazy[node * 2 + 1] = 1
            return

        mid = (start + end) // 2
        self._update_range(node * 2, start, mid, l, r)
        self._update_range(node * 2 + 1, mid + 1, end, l, r)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def update_range(self, l, r):
        self._update_range(1, 1, self.n, l, r)

    def _query_range(self, node, start, end, l, r):
        if self.lazy[node] != 0:
            self.tree[node] = (end - start + 1)
            if start != end:
                self.lazy[node * 2] = 1
                self.lazy[node * 2 + 1] = 1
            self.lazy[node] = 0

        if start > end or start > r or end < l:
            return 0

        if start >= l and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        left_query = self._query_range(node * 2, start, mid, l, r)
        right_query = self._query_range(node * 2 + 1, mid + 1, end, l, r)
        return left_query + right_query

    def query_range(self, l, r):
        return self._query_range(1, 1, self.n, l, r)

class CountIntervals:
    def __init__(self):
        self.st = SegmentTree(10**9)  # Assuming the range [1, 10^9]
    
    def add(self, left: int, right: int) -> None:
        self.st.update_range(left, right)
    
    def count(self) -> int:
        return self.st.query_range(1, 10**9)

# Example usage
ci = CountIntervals()
ci.add(1, 3)
ci.add(5, 7)
print(ci.count())  # Output: 6 (1, 2, 3, 5, 6, 7)
ci.add(2, 6)
print(ci.count())  # Output: 7 (1, 2, 3, 4, 5, 6, 7)

'''
Time and Space Complexity

    Time Complexity:
        Update Operation: O(logn), where n is the size of the range.
        Query Operation: O(logn).

    Space Complexity:
        Segment Tree: O(4n), where n is the size of the range.
        Lazy Propagation Array: O(4n).

Considerations

    Range Size: The segment tree size and lazy array should be large enough to cover the range of inputs.
    Lazy Propagation: Correct handling of lazy propagation is crucial for maintaining efficiency.
    Initialization: Proper initialization of the tree and lazy arrays is necessary to avoid bugs.
    Edge Cases: Consider edge cases such as overlapping intervals, intervals touching boundaries, etc.

Conclusion

Segment trees provide a powerful and efficient way to handle range queries and updates. By using lazy propagation, we can further optimize the update operations. This approach is particularly useful for large datasets where frequent updates and queries are required. If you have any further questions or need additional explanations, feel free to ask!
'''