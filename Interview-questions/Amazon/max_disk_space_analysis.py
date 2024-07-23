from collections import deque

def max_of_sliding_window_minimums(arr, k):
    n = len(arr)
    if n == 0 or k == 0:
        return 0
    
    # Deque to store indices of elements in the current window
    deq = deque()
    
    # List to store the minimums of all sliding windows
    min_of_windows = []
    
    # Process first k elements to initialize the deque
    for i in range(k):
        while deq and arr[deq[-1]] >= arr[i]:
            deq.pop()
        deq.append(i)
    
    # Process the rest of the elements
    for i in range(k, n):
        # The element at the front of the deque is the minimum of the previous window
        min_of_windows.append(arr[deq[0]])
        
        # Remove elements that are out of the current window
        while deq and deq[0] <= i - k:
            deq.popleft()
        
        # Maintain the decreasing order in deque
        while deq and arr[deq[-1]] >= arr[i]:
            deq.pop()
        
        # Add the current element at the end of deque
        deq.append(i)
    
    # Add the minimum for the last window
    min_of_windows.append(arr[deq[0]])
    
    # Return the maximum of the minimums
    return max(min_of_windows)

# Example usage
disk_spaces = [8, 2, 4, 6, 7, 3, 5, 1]
window_size = 3
max_min_disk_space = max_of_sliding_window_minimums(disk_spaces, window_size)
print("Maximum of the minimums in all sliding windows:", max_min_disk_space)
