# graph = dict()
graph = {
    'A' : ['B','C'],
    'B' : ['D', 'E'],
    'C' : ['F'],
    'D' : [],
    'E' : ['F'],
    'F' : []
}

def bfs(src,dst,graph):
    path_list = list()
    visited = set()
    queue = list()
    
    # store current node and path
    node = src 
    path = [src]
    queue.append([node,path])
    
    if src==dst:
        print("same node")
        path_list.append(src)
        return path_list
    
    # start exploring
    
    while queue:
        node,path_list = queue.pop(0)
        if node not in visited:
            neighbours = graph[node]
            for neighbour in neighbours:
                new_path_list = path_list + [neighbour]
                queue.append([neighbour,new_path_list])
                
                # if reached at destination 
                if neighbour == dst :
                    return new_path_list
                
        visited.add(node)
        
    print("No path found")
    return None 


if __name__=='__main__':
    src = 'A'
    dst = 'F'
    
    path = bfs(src,dst,graph=graph)
    if path:
        print(path)
        