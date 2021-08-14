class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        def bruteforce():
            for i in range(9):
                for j in range(9):
                    boxr, boxc = i//3 , j//3
                    num = board[i][j]
                    if num=='.':
                        continue
                    # check if it's in column (j is fixed)
                    for k in range(9):
                        if k==i:
                            continue
                        else :
                            if board[k][j]==num:
                                # print(num)
                                return False
                    # check if it's in row (i is fixed)
                    for k in range(9):
                        if k==j:
                            continue
                        else :
                            if board[i][k]==num:
                                # print(num)
                                return False

                    # check if it's in box
                    for m in range(boxr*3,boxr*3+3):
                        for n in range(boxc*3,boxc*3+3):
                            if m==i and n==j:
                                continue
                            else :
                                if board[m][n]==num:
                                    # print(num)
                                    return False
            return True
        
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
                            # print(i,'row is fixed',k)
                            return False
                        if board[k][j]==num and k!=i:
                            # print(i,'col is fixed',k)
                            return False
                    for r in range(boxr,boxr+3):
                        for c in range(boxc,boxc+3):
                            if r==i and c==j:
                                continue
                            currnum = board[r][c]
                            if currnum==num :#and r!=i and c!=j:
                                return False
            return True
        
        def testit():
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
            for i in range(n):
                for j in range(n):
                    if not check(i,j):
                        return False
            return True
        
        # return bruteforce()
        # return is_valid()
        return testit()
                
        