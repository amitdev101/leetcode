from typing import List
class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        n = 9
        def check(r,c):
            num = board[r][c]
            if num=='.':
                return True
            for i in range(n):
                if board[r][i]== num and i!=c:
                    return False
                if board[i][c]==num and i!=r:
                    return False
            boxr, boxc = 3*(r//3), 3*(c//3)
            # check box 
            for i in range(boxr,boxr+3):
                for j in range(boxc,boxc+3):
                    if i==r and j==c:
                        continue
                    else:
                        if board[i][j] == num:
                            return False
            return True
        
        def solveit(r=0,c=0):
            print(f'Row = {r}, Col = {c}')
            # base condition
            if r==n:
                print("Got solved")
                
                return True
            num = board[r][c]
            nc=c+1
            nr = r
            if nc==n:
                nr+=1
                nc=0
            if num=='.':
                for i in range(1,n+1):
                    board[r][c]=str(i)
                    if check(r,c):
                        if solveit(nr,nc):
                            return True
                            
                    # reverse the state
                    board[r][c]='.'
            else :
                return solveit(nr,nc)
                
            return False
        
        solveit()
                    
                    
                
                
                        
                            
                
                        
                    
                    
        