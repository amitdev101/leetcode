from typing import List

class Solution:
    def solveSudoku(self, board: List[List[str]]) -> None:
        """
        Do not return anything, modify board in-place instead.
        """
        n = 9
        def is_valid():
            for i in range(n):
                for j in range(n):
                    num = board[i][j]
                    if num=='.':
                        continue
                    boxr,boxc = 3*(i//3), 3*(j//3)
                    # check if valid row (row is constant)
                    for k in range(n):
                        if board[i][k]==num and k!=j:
                            return False
                        if board[k][j]==num and k!=i:
                            return False
                    for r in range(boxr,boxr+3):
                        for c in range(boxc,boxc+3):
                            currnum = board[r][c]
                            if i==r and j==c:
                                continue
                            if currnum==num:
                                return False
            return True
        
        def brutesolve(r=0,c=0):
            print(f'Row={r} Col={c}')
            # base case
            if r==n :
                return True
            # recursive cases
            
            # search for an empty location
            if board[r][c]=='.':
                for i in range(1,n+1):
                    board[r][c]=str(i)
                    if is_valid():
                        if c+1==n:
                            nr=r+1
                            nc=0
                        else :
                            nr = r
                            nc = c+1
                        if brutesolve(nr,nc)==True:
                            return True
                        
                    # reversing the state (necessary for recusion)
                    board[r][c]='.'
            else :
                if c+1==n:
                    nr=r+1
                    nc=0
                else :
                    nr = r
                    nc = c+1
                return brutesolve(nr,nc)
                
                
        brutesolve()
                    
                
def test():
    board = [[".",".","9","7","4","8",".",".","."],["7",".",".",".",".",".",".",".","."],[".","2",".","1",".","9",".",".","."],[".",".","7",".",".",".","2","4","."],[".","6","4",".","1",".","5","9","."],[".","9","8",".",".",".","3",".","."],[".",".",".","8",".","3",".","2","."],[".",".",".",".",".",".",".",".","6"],[".",".",".","2","7","5","9",".","."]]
    sol = Solution()
    print(sol.solveSudoku(board))

test()
                        
                            
                
                        
                    
                    
        