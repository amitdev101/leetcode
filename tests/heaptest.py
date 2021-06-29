from heapq import *
import random
pq = []

numbers = [random.randint(0,100) for i in range(10)]

for number in numbers:
    heappush(pq,(number,number*100,str(number)))

p = heappop(pq)

print(p) # will return the tuple