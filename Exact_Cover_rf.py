'''
Refer to: 

https://gieseanw.wordpress.com/2011/06/16/solving-sudoku-revisited/

https://www.ocf.berkeley.edu/~jchu/publicportal/sudoku/sudoku.paper.html

For explanation of the algorithm

There will be 324 columns, the types of which are:
- num_in_row for values 1-9 (81)
- num_in_col for values 1-9 (81)
- num_in_box for values 1-9 (81)
- cell_used for each of the 9x9 cells (81)

Each column is a constraint that must be fulfilled

There will be 729 rows, one for each possible state of each of the 9x9 cells, i.e. 9x9x9

Algorithm X will eliminate each column and recursively backtrack when it reaches a dead-end where not all the constraints can be fulfilled

'''
# RECROAKEN

import time, collections
from copy import deepcopy

problem_board = [
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

def find_completed_cells(board):
	completed_cells = [(i_row*9 + i_col + 1, col) for i_row, row in enumerate(board) for i_col, col in enumerate(row) if col != 0]
	return completed_cells

def find_row_num(cell_num):
		return (cell_num - 1) // 9 + 1

def find_col_num(cell_num):
		return ((cell_num % 9) or 9)

def find_box_num(cell_num):
	return [[1,2,3], [4,5,6], [7,8,9]][(find_row_num(cell_num) - 1) // 3][(find_col_num(cell_num) - 1) // 3]

class col_header(object):
	def __init__(self, col_type, type_val, cell_val = None):
		'''
		type takes 'num_in_row', 'num_in_col', 'num_in_box', 'cell_used' as inputs
		type_val takes 1-9 and 1-81 as inputs. 1-81 is for when col_type is 'cell_used' only.
		cell_value takes 1-9 as inputs and is used only when the col_type is 'num_in_row', 
		'num_in_col' or 'num_in_box'
		'''

		self.col_type = col_type
		self.type_val = type_val
		self.cell_val = cell_val
		self.nodes = dict()
		self.id = ("Column Header", col_type, type_val, cell_val)
		self.nodes['col_header'] = self

	def __str__(self):
		strs = {
				'num_in_row': "Is {} used in row {}?".format(self.cell_val, self.type_val),
				'num_in_col': "Is {} used in column {}?".format(self.cell_val, self.type_val),
				'num_in_box': "Is {} used in box {}?".format(self.cell_val, self.type_val),
				'cell_used': "Is cell {} used?".format(self. type_val),
				None: "This is the root header node"
		}
		return strs[self.col_type]

	def link(self, direction, node):
		self.nodes[direction] = node

	def get(self, direction):
		return self.nodes[direction] 

class row_node(object):
	def __init__(self, col_type, type_val, cell_val = None):
		self.col_type = col_type
		self.type_val = type_val
		self.cell_val = cell_val
		self.id = ("Row Node", col_type, type_val, cell_val)
		self.nodes = dict()

	def __str__(self):
		strs = {
				'num_in_row': "{} used in row {}".format(self.cell_val, self.type_val),
				'num_in_col': "{} used in column {}".format(self.cell_val, self.type_val),
				'num_in_box': "{} used in box {}".format(self.cell_val, self.type_val),
				'cell_used': "Cell {} used".format(self.type_val),
				'row_header': "This is a row header for Cell {} with value {}".format(self.type_val, self.cell_val)
		}
		return strs[self.col_type]

	def link(self, direction, node):
		self.nodes[direction] = node

	def get(self, direction):
		return self.nodes[direction]


def create_column_headers(root):
	'''
	There will be 324 columns, the types of which are:
	- num_in_row for values 1-9 (81)
	- num_in_col for values 1-9 (81)
	- num_in_box for values 1-9 (81)
	- cell_used for each of the 9x9 cells (81)

	This function creates a horizontally linked list of column header nodes and returns
	a dictionary, where each column header node can be accessed through its id
	'''

	headers = collections.OrderedDict()
	headers['start'] = root
	# create headers for num_in_row
	current_header = root


	for col_type in ['num_in_row', 'num_in_col', 'num_in_box']:
		for type_val in range(1, 10):
			for cell_val in range(1, 10):
				# establish new_header, add it to dict, and add the appropriate linkages
				new_header = col_header(col_type, type_val, cell_val)
				headers[new_header.id] = new_header
				
				new_header.link('up', new_header)
				new_header.link('down', new_header)

				current_header.link('right', new_header)
				new_header.link('left', current_header)

				current_header = new_header

	for type_val in range(1, 82):
		new_header = col_header('cell_used', type_val)
		headers[new_header.id] = new_header

		new_header.link('up', new_header)
		new_header.link('down', new_header)

		current_header.link('right', new_header)
		new_header.link('left', current_header)

		current_header = new_header


	current_header.link('right', root)
	root.link('left', current_header)

	return headers


def get_all_nodes(any_node, axis):
	'''
	Utility function to see all the nodes in a linked list for a specific axis: 
	horizontal or vertical

	Returns all nodes, including starting node and header nodes
	'''
	seen = {any_node} # any_node.id is not used here, as the same id will appear for all nodes in a column

	if axis == 'horizontal':
		curr_node = any_node.get('right')
		while curr_node not in seen:
			seen.add(curr_node)
			curr_node = curr_node.get('right')
		return seen
	elif axis == 'vertical':
		curr_node = any_node.get('down')
		while curr_node not in seen:
			seen.add(curr_node)
			curr_node = curr_node.get('down')
		return seen
	else:
		raise ValueError

def add_node_to_column(headers, new_node):
	'''
	Adds the new_node to the end of the linked list. Since linked list is circular,
	this means the new_node is effectively the one that now precedes the col_header_node
	'''
	col_header = headers[tuple(["Column Header"] + list(new_node.id)[1:])]

	new_node.link('up', col_header.get('up'))
	col_header.get('up').link('down', new_node)

	new_node.link('down', col_header)
	col_header.link('up', new_node)

	new_node.link('col_header', col_header)

def create_nodes_for_row(headers, rows, cell_num, cell_val):
	# For one of the 729 rows, create 4 row_nodes + 1 row_header to represent
	# the constraints being fulfilled
	col_types = ['num_in_row', 'num_in_col', 'num_in_box', 'cell_used']
	type_val_func = {
				'num_in_row': find_row_num,
				'num_in_col': find_col_num,
				'num_in_box': find_box_num,
				'cell_used': int
				}

	# Create row_header
	row_header = row_node('row_header', cell_num, cell_val)
	rows[row_header.id] = row_header
	curr_node = row_header # placeholder node, to ease the circular-linking

	# Create the 4 row_nodes
	for col_type in col_types:
		if col_type == 'cell_used': cell_val = None
		new_node = row_node(col_type, type_val_func[col_type](cell_num), cell_val)
		add_node_to_column(headers, new_node)

		curr_node.link('right', new_node)
		new_node.link('left', curr_node)
		new_node.link('row_header', row_header)

		curr_node = new_node

	curr_node.link('right', row_header)
	row_header.link('left', curr_node)

def create_rows(headers):
	'''
	For each of the 729 cell possibilities (81 * 9), a row of nodes will be created.

	Each row consists of 4 nodes, corresponding to the 4 constraints fulfilled, namely:
	num_in_row
	num_in_col
	num_in_box
	cell_used

	There will be 729 * 4 = 2916 row_nodes created in total.
	'''

	rows = dict() # use len() to confirm there are 729 rows

	for cell_num in range(1, 82):
		for cell_val in range(1, 10):
			create_nodes_for_row(headers, rows, cell_num, cell_val)

	return rows	

def remove_node(node, axis):
	'''
	Removes a node from its linked list (horizontal or vertical)
	Does not change the linkages on the node itself
	'''

	if axis == 'horizontal':
		node.get('left').link('right', node.get('right'))
		node.get('right').link('left', node.get('left'))

	elif axis == 'vertical':
		node.get('up').link('down', node.get('down'))
		node.get('down').link('up', node.get('up'))

def readd_node(node, axis):
	'''
	Restores a node to its original place in a linked list
	'''
	if axis == 'horizontal':
		node.get('left').link('right', node)
		node.get('right').link('left', node)
	elif axis == 'vertical':
		node.get('up').link('down', node)
		node.get('down').link('up', node)

def cover(Node):
	if Node.col_type != 'row_header':  #basically skipping over any row_header nodes
		col_header = Node.get('col_header')
		remove_node(col_header, 'horizontal')

		row_node = col_header.get('down')

		while row_node != col_header:
			right_node = row_node.get('right')
			while right_node != row_node:
				if right_node.col_type != 'row_header':
					remove_node(right_node, 'vertical')
				right_node = right_node.get('right')
			row_node = row_node.get('down')

def uncover(Node):
	if Node.col_type != 'row_header':
		col_header = Node.get('col_header')
		readd_node(col_header, 'horizontal')

		row_node = col_header.get('down')

		while row_node != col_header:
			right_node = row_node.get('right')

			while right_node != row_node:
				if right_node.col_type != 'row_header':
					readd_node(right_node, 'vertical')
				right_node = right_node.get('right')
			row_node = row_node.get('down')

def printSolution(problem_board, solutions):
	'''
	All steps taken in the solving step will be recorded in the list 'solutions'
	Each addition will be reflected in the original problem_board
	The completed board is then printed.

	solutions is a list of row_header_nodes, id: ("Row Node", col_type, type_val, cell_val)
	'''
	for s in solutions:
		problem_board[find_row_num(s.type_val) - 1][find_col_num(s.type_val) - 1] = s.cell_val

	for row in problem_board:
		print(row)


def sudoku_solver(problem_board):
	h = col_header(None, None) # the first header node, non-constraint.
	headers = create_column_headers(h)

	rows = create_rows(headers)


	completed_cells = find_completed_cells(problem_board)

	for cell in completed_cells:
		row_header = rows[('Row Node', 'row_header', cell[0], cell[1])]

		right_node = row_header.get('right')

		while right_node != row_header:
			cover(right_node)
			right_node = right_node.get('right')



	solutions = []

	def solve(h, solutions):
		#printSolution(deepcopy(problem_board), solutions)
		
		if h.get('right') == h:
			return True
		else:
			column_node = h.get('right')
			cover(column_node)

			row_node = column_node.get('down')

			while row_node != column_node:
				solutions.append(row_node.get('row_header'))

				right_node = row_node.get('right')
				while right_node != row_node:
					cover(right_node)
					right_node = right_node.get('right')
				if solve(h, solutions):
					return True

				solutions.pop() # discard solution

				left_node = row_node.get('left')
				while left_node != row_node:
					uncover(left_node)
					left_node = left_node.get('left')

				row_node = row_node.get('down')

			uncover(column_node)

			return False

	if solve(h, solutions):
		printSolution(problem_board, solutions)
	else:
		print("No solutions found")

tic = time.time()

sudoku_solver(problem_board)

print("Total time elapsed: {}".format(time.time() - tic))

