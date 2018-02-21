from board import *
import algo

class player:
	AI_player = 0

	def __init__(self, board, bango):
		self.board = board
		self.bango = bango

	def play(self):
		print(self.board)
		self.place()
		over = self.board.over()
		if over:
			print('X' if self.bango == 1 else 'O', 'wins!')
		return over

	def place(self):
		raise NotImplementedError

class keyboard_player(player):

	def place(self):
		while True:
			raw = input('Place your move:')
			if raw == 'exit':
				exit()
			try:
				pos = raw.split(' ')
				pos = (int(pos[0]), int(pos[1]))
				self.board.place((self.bango, pos))
				break
			except EOFError:
				print()
				exit()
			except:
				print('Invalid input format!')


class AI(player):

	def place(self):
		while True:
			if player.AI_player < 2:
				order = input('Input any words to continue:')
				if order == 'exit':
					exit()
				elif order == 'undo':
					self.board.undo()
					return
				elif order == 'snapshot':
					name = input('Input file name:')
					f = open(name, 'w')
					print(self.board.moves, file = f)
			try:
				board = self.board.get_board()
				#print("Get after get board")
				moves = {}
				for i in range(len(board)):
					for j in range(len(board)):
						if board[i][j]:
							moves[i, j] = board[i][j]
				#print("finish generate moves")
				print("Looking for next move........")
				pos = algo.place(self.bango, self.board.size, moves, self.board, 4)
				self.board.place((self.bango, pos))
				print("Move chosen: ", (self.bango, pos))
				break
			except Exception as ex:
				print(ex)
				print('AI failed!')
				exit()
