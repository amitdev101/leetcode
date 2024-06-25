from typing import List
# https://leetcode.com/problems/number-of-islands/ 

class UnionFind:
        def __init__(self, size):
            self.parent = [i for i in range(size)]
            self.rank = [0]*size # this defines number of children
            self.count = 0 # count of distinct set/island

        def find(self, x):
            if self.parent[x] != x:
                self.parent[x] = self.find(self.parent[x]) # path compression
            return self.parent[x] 

        def union(self, x, y):
            rootX = self.find(x)
            rootY = self.find(y)
            if rootX != rootY:
                if self.rank[rootX] > self.rank[rootY]:
                    self.parent[rootY]= rootX
                elif self.rank[rootX] < self.rank[rootY]:
                    self.parent[rootX] = rootY
                else:
                    self.parent[rootY] = rootX
                    self.rank[rootX] += 1
                self.count -= 1

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        # return self.bfs_solution(grid)
        rows, cols = len(grid), len(grid[0])
        uf = UnionFind(rows*cols)
        count = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c]=='1':
                    count += 1
                    uf.count += 1
                    grid[r][c] = '0' # mark as visited
                    for dr, dc in [(0,1), (1,0)]: # checking right and down only to avoid duplicate calculation.
                        nr, nc = r+dr, c+dc
                        if 0<= nr < rows and 0 <=nc < cols and grid[nr][nc] == '1':
                            uf.union(r*cols + c, nr*cols + nc)
        return uf.count

    
 
                



        