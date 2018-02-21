class board:

	def __init__(self, size):
		self.size = size
		self.__board = []
		self.last_step = None
		self.moves = []
	# Initialize the board:
	# self.__board[i][j] is 0 when there is no 
	# stone on it, equals 1 otherwise
		for i in range(size):
			l = []
			for j in range(size):
				l.append(0)
			self.__board.append(l)

	def __str__(self):
		string = ' ' + ''.join([' ' + str(i % 10) for i in range(self.size)]) + '\n'
		string += ''.join([str(i % 10) + ''.join([
			'─┼' if not self.__board[i][j] else
			'─X' if self.__board[i][j] == 1 else '─O'
			for j in range(self.size)
		]) + '\n' for i in range(self.size)])
		'''
		string = ""
		for i in range(2*self.size):
			for j in range(2*self.size):
				if i % 2 ==0:
					# The first line
					if i == 0:
						if j % 2 == 1:
							index = (j-1)//2
							string += "%2d" % (index)
						else:
							string += ' '
					# Not the first row but is even row
					else:
						if j % 2 == 0:
							string += '  '
						else:
							string += '|'
				# Odd row
				else:
					if j % 2 == 0:
						if j == 0:
							string += "%2d" % ((i-1)//2)
						else:
							string += '──'
					else:
						if self.__board[(i-1)//2][(j-1)//2] == 0:
							string += '┼'
						elif self.__board[(i-1)//2][(j-1)//2] == 1:
							string += '⚫'
						elif self.__board[(i-1)//2][(j-1)//2] == 2:
							string += '⚪'
						else:
							raise Exception("Invalid stone value")
				if j == 2*self.size - 1:
					string += '\n'
		'''
		return string


	def place(self, coordinate):
		# TODO: Check if the player has wrong placement
		#print(coordinate)
		if coordinate[0] > 2 or coordinate[0] < 1:
			raise Exception("Invalid Input")
		if self.__board[coordinate[1][0]][coordinate[1][1]] == 0:
			self.__board[coordinate[1][0]][coordinate[1][1]] = coordinate[0]
			# Remember the latest step to help over method
			self.last_step = tuple(coordinate)
			self.moves.append(coordinate)
		else:
			# TODO: raise exception, don't remember the function name
			raise Exception("Invalid Place: piece already exists")

	def over(self):
		"""
		0: No winner detected and game is not over
		1: Winner detected
		2: Draw detected
		"""
		if self.last_step == None:
			return False
		color = self.last_step[0]
		possbile_combs = self.calculate_coord()
		for comb in possbile_combs:
			flag = 1
			for coord in comb:
				if self.__board[coord[0]][coord[1]] != color:
					flag = 0
					break
			if flag == 1:
				break
		if flag == 1:
			return flag
		for row in self.__board:
			for col in row:
				if col == 0:
					return 0
		return 2
	def calculate_coord(self):
		coord = self.last_step[1]
		possbile_comb = []
		horizental = []
		vertical = []
		for i in range(-4,5):
			horizental.append([coord[0], coord[1] + i])
			vertical.append([coord[0] + i, coord[1]])
		for i in range(5):
			if horizental[i][1] >= 0 and horizental[i+4][1] < self.size:
				possbile_comb.append(horizental[i:i+5])
			if vertical[i][0] >= 0 and vertical[i+4][0] < self.size:
				possbile_comb.append(vertical[i:i+5])
		slash = []
		#     /
		#    /
		#   /
		#  /
		# /
		backslash = []
		#\
		# \
		#  \
		#   \
		#    \
		for i in range(-4, 5):
			slash.append([coord[0] - i, coord[1] + i])
			backslash.append([coord[0] + i, coord[1] + i])
		for i in range(5):
			if slash[i][0] < self.size and slash[i][1] >= 0 and \
				slash[i+4][0] >= 0 and slash[i+4][1] < self.size:
				possbile_comb.append(slash[i:i+5])
			if backslash[i][0] >= 0 and backslash[i][1] >= 0 and \
				backslash[i+4][0] < self.size and backslash[i+4][1] < self.size:
				possbile_comb.append(backslash[i:i+5])
		return possbile_comb

	def get_board(self):
		return list(self.__board)

	def get_last_step(self):
		if self.last_step == None:
			return None
		return tuple(self.last_step)

	def undo(self):
		if len(self.moves) != 0:
			#print("undo board for move:{}".format(self.last_step))
			self.__board[self.last_step[1][0]][self.last_step[1][1]] = 0
			self.moves.pop()
			if len(self.moves) > 0:
				self.last_step = self.moves[-1]
			else:
				self.last_step = None
		else:
			print("Board is empty, cannot undo!")
	




if __name__ == '__main__':
	test_board = Board(15)
	test_board.place((1,(0,0)))
	test_board.place((2,(0,14)))
	print(test_board.over())
	print(test_board)
