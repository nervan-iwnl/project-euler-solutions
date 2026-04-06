from __future__ import annotations
from typing import List

class SudokuSolver:
    
    def __init__(self):
        self.board = []
    
    def set_board(self, board: list[list[int]]) -> None:
        self.board = board 
    
    def __is_valid(self, r: int, c: int, val: int) -> bool:
        for j in range(9):
            if self.board[r][j] == val:
                return False
            
            if self.board[j][c] == val:
                return False

        br = (r // 3) * 3
        bc = (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if self.board[i][j] == val:
                    return False
        return True

    def __find_empty(self) -> tuple[int, int] | None:
        for r in range(9):
            for c in range(9):
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve(self):
        empty = self.__find_empty()
        if empty is None:
            return True

        r, c = empty
        for val in range(1, 10):
            if self.__is_valid(r, c, val):
                self.board[r][c] = val
                
                if self.solve():
                    return True
                
                self.board[r][c] = 0
        return False
                  
    
def parse_sudoku() -> List[List[int]]:
    puzzles = []
    with open('sudoku.txt') as f:        
        lines = [line.strip() for line in f if line.strip()]
    
    for i in range(0, len(lines), 10):
        board = []
        for row in lines[i + 1:i + 10]:
            board.append([int(ch) for ch in row])
        puzzles.append(board)

    return puzzles

        
def solve():
    ss = SudokuSolver()
    puzzles = parse_sudoku()
    ans = 0
    for puz in puzzles:
        ss.set_board(puz)
        ss.solve()
        ans += ss.board[0][0] * 100 + ss.board[0][1] * 10 + ss.board[0][2]
    return ans

if __name__ == "__main__":
    print(solve())
