#Test.it("I wish you good luck!")

problem = [
		[1, 0, 0, 0, 0, 7, 0, 9, 0],
		[0, 3, 0, 0, 2, 0, 0, 0, 8],
		[0, 0, 9, 6, 0, 0, 5, 0, 0],
		[0, 0, 5, 3, 0, 0, 9, 0, 0],
		[0, 1, 0, 0, 8, 0, 0, 0, 2],
		[6, 0, 0, 0, 0, 4, 0, 0, 0],
		[3, 0, 0, 0, 0, 0, 0, 1, 0],
		[0, 4, 1, 0, 0, 0, 0, 0, 7],
		[0, 0, 7, 0, 0, 0, 3, 0, 0]
		]

#solution = [[9, 2, 6, 5, 8, 3, 4, 7, 1], [7, 1, 3, 4, 2, 6, 9, 8, 5], [8, 4, 5, 9, 7, 1, 3, 6, 2], [3, 6, 2, 8, 5, 7, 1, 4, 9], [4, 7, 1, 2, 6, 9, 5, 3, 8], [5, 9, 8, 3, 1, 4, 7, 2, 6], [6, 5, 7, 1, 3, 8, 2, 9, 4], [2, 8, 4, 7, 9, 5, 6, 1, 3], [1, 3, 9, 6, 4, 2, 8, 5, 7]]

def print_board(board):
	# Utility function to see board progress
	if not isinstance(board, list): 
		print(board)
	else:
		for row in board:
			print(row)

import functools

# KEWL 

def find_empty_cell(board):
	dim = len(board)
	for r in range(dim):
		for c in range(dim):
			if board[r][c] == 0:
				return [r, c]
	return None

def possibles(board, row, col):
	row_values = set(board[row])
	col_values = set([board[r][col] for r in range(9)])
	box_values = set([board[(row//3)*3 + i][(col//3)*3 + j] for i in range(3) for j in range(3)])
	return list(set(range(1, 10)) - row_values - col_values - box_values)


def sudoku_solver(board):
    if len(board) != 9: raise ValueError
    for row in board:
        if len(row) != 9: raise ValueError
        
    all_numbers = functools.reduce(lambda x, y: x.union(y), [set(row) for row in board])
    
    if len(all_numbers - set(range(10))) > 0: raise ValueError
    
    def solve(board):
    	l = find_empty_cell(board)
        
    	if not l: return True
    	for p in possibles(board, l[0], l[1]):
    
    		board[l[0]][l[1]] = p
    		if solve(board):
    			return True
    		board[l[0]][l[1]] = 0
    	return False
    	
    if solve(board):
        return board
    else:
    	return "No solution exists."

import time

tic = time.time()

print_board(sudoku_solver(problem))

print(time.time() - tic)