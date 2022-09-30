from typing import List 
from collections import defaultdict, deque

def topological_sort(tasks_list: List[List[int]]):
    graph = dict()
    indegree = dict()
    q = list()
    ans = list()

    # building graph and finding indegree
    for tasks in tasks_list:
        task, dependency = tasks
        if not dependency in graph:
            graph[dependency] = list()
        graph[dependency].append(task)
        
        if not task in indegree:
            indegree[task]=0
        indegree[task]+=1
        
        if not dependency in indegree:
            indegree[dependency]=0
        
            
    # topology
    for key in indegree:
        degree = indegree[key]
        if degree ==0:
            q.append(key)
    
    while q:
        task_done = q.pop(0)
        ans.append(task_done)
        if task_done in graph:
            for dependent in graph[task_done]:
                indegree[dependent]-=1
                if indegree[dependent]==0:
                    q.append(dependent)
                    
    # check whether all tasks are done or not
    for key in indegree:
        if indegree[key] > 0:
            return []
    return ans
        
if __name__=='__main__':
    str_prerequistes = [['a', 'b'], ['a', 'c'], ['a', 'd'],[None,'e']] # Here e is independent task
    print(topological_sort(str_prerequistes))
    
    prerequistes = [[1, 0], [2, 0], [3, 1], [3, 2]]
    print(topological_sort(prerequistes))
        