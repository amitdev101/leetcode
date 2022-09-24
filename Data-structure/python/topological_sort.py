# Algorithm

# The algorithm of the topological sort goes like this:

#     Identify the node that has no in-degree(no incoming edges) and select that node as the source node of the graph
#     Delete the source node with zero in-degree and also delete all its outgoing edges from the graph. Insert the deleted vertex in the result array.
#     Update the in-degree of the adjacent nodes after deleting the outgoing edges
#     Repeat step 1 to step 3 until the graph is empty

# The resulting array at the end of the process is called the topological ordering of the directed acyclic graph. If due to some reason, there are some nodes left but they have the incoming edges, that means that the graph is not an acyclic graph and topological ordering does not exist.
# Python Code For Topological Sort

from collections import defaultdict

class Graph:

    def __init__(self,n):

        self.graph = defaultdict(list)

        self.N = n

    def addEdge(self,m,n):

        self.graph[m].append(n)

    def sortUtil(self,n,visited,stack):

        visited[n] = True

        for element in self.graph[n]:

            if visited[element] == False:

                self.sortUtil(element,visited,stack)

        stack.insert(0,n)

    def topologicalSort(self):

        visited = [False]*self.N

        stack =[]

        for element in range(self.N):

            if visited[element] == False:

                self.sortUtil(element,visited,stack)

        print(stack)

graph = Graph(5)
graph.addEdge(0,1);
graph.addEdge(0,3);
graph.addEdge(1,2);
graph.addEdge(2,3);
graph.addEdge(2,4);
graph.addEdge(3,4);

print("The Topological Sort Of The Graph Is:  ")

graph.topologicalSort()

