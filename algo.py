import math
import os
from board import *

WIN = 666666
LOSE = 66666
WIN2 = 6666
LOSE2 = 666

class state:
	N = 0

	def __init__(self, bango, limit, moves, last_move = None, score = 0):
		self.bango = bango
		self.limit = limit
		self.moves = moves
		self.children = None
		self.value = 0
		self.visit_times = 0
		self.win_times = 0
		self.lose_times = 0
		self.draw_times = 0
		self.last_move = last_move
		self.score = score

	def successors(self):
		return [state(3 - self.bango, self.limit,
					  dict(self.moves.items() | {move: self.bango}.items()), 
					  (self.bango, move), -score)
				for score, move in self.next_moves()]

	def best_successor(self):
		next_moves = [x[1] for x in self.next_moves()]
		return state(3 - self.bango, self.limit,
					 dict(self.moves.items() | {next_moves[0]: self.bango}.items()),
					 (self.bango, next_moves[0]))

	def next_moves(self, num = 5):
		"""
		Return a list of 8 most possible next moves
		"""
		if len(self.moves) == 0:
			return [(0, (self.limit // 2, self.limit // 2))]

		scores = {}
		for i, j in self.moves:
			for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]:
				p, q = i + x, j + y
				if 0 <= p < self.limit and 0 <= q < self.limit and (p, q) not in self.moves:
					scores[p, q] = 0

		for p, q in scores:
			for x, y in [(1, 0), (0, 1), (1, 1), (1, -1)]:
				cont, tail, dire = [None, 0, 0], [None, 0, 0], [None, 0, 0]

				s, t = p + x, q + y
				if (s, t) in self.moves:
					bango = self.moves[s, t]
					dire[bango] += 1
					s, t = s + x, t + y
					while (s, t) in self.moves and self.moves[s, t] == bango:
						cont[bango] += 1
						s, t = s + x, t + y
					if (s, t) not in self.moves and 0 <= s < self.limit and 0 <= t < self.limit:
						tail[bango] += 1

				s, t = p - x, q - y
				if (s, t) in self.moves:
					bango = self.moves[s, t]
					dire[bango] += 1
					s, t = s - x, t - y
					while (s, t) in self.moves and self.moves[s, t] == bango:
						cont[bango] += 1
						s, t = s - x, t - y
					if (s, t) not in self.moves and 0 <= s < self.limit and 0 <= t < self.limit:
						tail[bango] += 1

				if cont[self.bango] + dire[self.bango] >= 4:
					scores[p, q] += WIN
				elif cont[3 - self.bango] + dire[3 - self.bango] >= 4:
					scores[p, q] += LOSE
				elif cont[self.bango] + tail[self.bango] >= 3:
					scores[p, q] += WIN2
				elif cont[3 - self.bango] + tail[3 - self.bango] >= 3:
					scores[p, q] += LOSE2
				else:
					a = cont[self.bango] + tail[self.bango]
					b = cont[3 - self.bango] + tail[3 - self.bango]
					scores[p, q] += max((a > 0) * 3 ** a + a,
										(b > 0) * 3 ** b)

		results = sorted([(-scores[coord], coord) for coord in scores])[0:num]
		return results

	def get_last_move(self):
		if self.last_move == None:
			return None
		return tuple(self.last_move)


	def check_over(self):
		pass

	def set_children(self, children, depth=0):
		copy_list = list(children)
		win_child = []
		lose_child = []
		win_child2 = []
		lose_child2 = []
		for child in children:
			#print("===============================\n")
			if child.score >= WIN:
				win_child.append(child)
				#if depth == 1:
					#print("Get fixed win list")
			elif child.score >= LOSE and len(copy_list) > 1:
				lose_child.append(child)
			elif child.score >= WIN2:
				win_child2.append(child)
			elif child.score >= LOSE and len(copy_list) > 1:
				lose_child2.append(child)
 				#if depth == 1:
					#print("Does remove someone with child prune:", child)
			"""
			else:
				for descendence in child.successors():
					print("Child deeper pruning: ", child)
					print("Prepare for checking descendence: ", descendence)
					l= self.prune_child(descendence)
					if len(l) == 0 and len(copy_list) > 1:
						copy_list.remove(child)
					if descendence.score == WIN and len(copy_list) > 1:
						copy_list.remove(child)
						if depth == 1:
							print("Does remove someone with descendents prune:", child)
						break
			"""
		if win_child:
			self.children = win_child
		elif lose_child:
			self.children = lose_child
		elif win_child2:
			self.children = win_child2
		elif lose_child2:
			self.children = lose_child2
		else:
			self.children = children

	def prune_child(self, descendence):
		children = descendence.successors()
		lst = list(children)
		for child in children:
			print("get child: {} of descendence: \n{}".format(child, descendence))
			print()
			if child.score == LOSE:
				lst.remove(child)
		return lst

	def get_children(self):
		return list(self.children)

	def get_mean_value(self):
		if self.visit_times == 0:
			return -1
		#elif self.lose_times == 0 and self.win_times != 0:
		#	return float("inf")
		#elif self.lose_times == 0 and self.win_times == 0:
			#return 0
		return self.win_times / self.visit_times

	def __lt__(self, other):
		a = self.get_mean_value()
		b = other.get_mean_value()
		return a < b

	def __str__(self):
		return "last_move:{} heuristic:{} visit times:{} score:{} win time:{} lose time:{} draw time:{}".format(
			self.last_move, self.score, self.visit_times, self.get_mean_value(), self.win_times, self.lose_times, self.draw_times)

	def get_move_pos(self):
		if self.last_move != None:
			return tuple(self.last_move[1])
		return None


def MC_search(curr_state, board, timebound=10):
	""" Applying Monte Carlo search within specific timebound """
	remain_time = timebound
	if curr_state.children == None:
		#print("No children detected:", curr_state)
		curr_state.set_children(curr_state.successors(), depth=1)
	if curr_state.last_move != None:
		board.undo()
	start_time = os.times()[0]
	stop_time = os.times()[0] + timebound
	flag = 0
	state.N = 0
	while os.times()[0] < stop_time:
		state.N += 1
		result = UCBF_single_search(curr_state, stop_time, board)
		# Check if we have at least reach the goal once
		if result != -1:
			flag = 1
	# TODO: Replace the psuedo code
	print("Totally do {} times MC search".format(state.N))
	if curr_state.last_move != None:
		board.place(curr_state.last_move)
	if flag == 1:
		return max(curr_state.get_children())
	else:
		print("Not even finish searching one path, need to justify the heuristic or search time")
		return curr_state.best_successor()





def UCBF_find_next(curr_state):
	""" Function that call UCBF_function() to find the child state we are to explore """
	# The case that state doesn't have the children
	if curr_state.children == None:
		curr_state.set_children(curr_state.successors())
	
	# child is a state class, children is a list of state class
	maxval_child = curr_state.children[0]
	maxval = UCBF_function(maxval_child)
	for child in curr_state.children:
		value = UCBF_function(child)
		if maxval < value:
			maxval_child = child
			maxval = value
	return maxval_child



def UCBF_function(curr_state, weight=2):
	""" Calculate the value of each state by using UCB function """
	# TODO: Figure out should add changing weight support
	if curr_state.visit_times == 0:
		return float("inf")
	else:
		value = curr_state.value/curr_state.visit_times + weight * math.sqrt(math.log(curr_state.N)/curr_state.visit_times)
		return value


def UCBF_single_search(curr_state, stop_time, board):
	if os.times()[0] > stop_time:
		return -1
	# Place the chess pieces first
	#print(curr_state)
	if curr_state.last_move != None:
		board.place(curr_state.last_move)
	p = board.over()
	# Check if the game has over in this node
	if p == 1:
		# Update the value and visit times
		curr_state.visit_times += 1
		curr_state.value += 1
		curr_state.win_times += 1
		board.undo()
		return curr_state.bango
	elif p == 2:
		curr_state.visit_times += 1
		curr_state.draw_times += 1
		board.undo()
		return 0 
	# If the game is not end, we then perform search
	# The end state should be leaf_node btw

	# Leaf node case
	if curr_state.children == None:
		# Case that first time we visit this node
		if curr_state.visit_times == 0:
			#print("Get visit times 0 leaf node")
			# UCBF_simulate will place the pieces again, so we undo
			# the move here to avoid Error
			board.undo()
			#print("Already undo the move")
			# Result is the var indicates which color wins the game
			result = UCBF_simulate(curr_state, stop_time, board)
			#print(result)
			#print(curr_state)
			if result == curr_state.bango:
				curr_state.value += 1
				curr_state.win_times += 1
			elif result == 3 - curr_state.bango:
				curr_state.lose_times += 1
			else:
				curr_state.draw_times += 1
			curr_state.visit_times += 1
			return result
		# Case that we have visited this node before
		else:
			state_to_simulate = UCBF_find_next(curr_state)
			result = UCBF_simulate(state_to_simulate, stop_time, board)
			#print(result)
			#print(state_to_simulate)
			if result == state_to_simulate.bango:
				state_to_simulate.value += 1
				state_to_simulate.win_times += 1
				curr_state.lose_times += 1
				#curr_state.value -= 1
			elif result == curr_state.bango:
				curr_state.value += 1
				state_to_simulate.lose_times += 1
				curr_state.win_times += 1
				#state_to_simulate.value -= 1
			elif result == 0:
				state_to_simulate.draw_times += 1
				curr_state.draw_times += 1
			state_to_simulate.visit_times += 1

	# Traverse the tree to the leaf node
	else:
		# call function to choose which child to search
		next_state = UCBF_find_next(curr_state)
		#print("Get next_state from find_next: ", next_state)
		result = UCBF_single_search(next_state, stop_time, board)
		#print(next_state)
		if curr_state.bango == result:
			curr_state.value += 1
			curr_state.win_times += 1
		elif curr_state.bango == 3 - result:
			curr_state.lose_times += 1
		elif result == 0:
			curr_state.draw_times += 1
	curr_state.visit_times += 1
	# Undo the move before quit the search
	if curr_state.last_move	!= None:
		board.undo()
	return result


def UCBF_simulate(curr_state, stop_time, board):
	if os.times()[0] > stop_time:
		return -1
	# Place the move
	board.place(curr_state.last_move)
	p = board.over()
	if p == 1:
		# Undo the move after simulation
		# Since we use the single board to perform simulation
		#print("Get win result in simulation")
		#print(board)
		board.undo()
		# This return value actually indicate who loses the game
		return curr_state.bango
	# Draw case
	elif p == 2:
		#print("Get draw result in simulation")
		#print(board)
		board.undo()
		return 0
	next_state = curr_state.best_successor()
	result = UCBF_simulate(next_state, stop_time, board)
	board.undo()
	return result
		


def place(bango, size, move, board, timebound):
	last_move = board.get_last_step()
	curr_state = state(bango, size, move, last_move)
	

	next_state = MC_search(curr_state, board, timebound)
	children = curr_state.get_children()
	for st in children:
		print(st)
	print("Finish MC search")
	pos = next_state.get_move_pos()
	if pos == None:
		raise Exception("Get pos for none, need to check implement")
	return pos



if __name__ == '__main__':
	tmp_dict = {(4, 7):2, (5, 7):2, (5,6):2, (6,5):2, (7,4):2,
				(8,3):1, (8,4):1, (8,6):1,(7,5):1, (6, 6):1, (3, 8):1}
	lst = [(1,(6, 6)), (2, (6, 5)), (1, (7, 5)), (2, (7,4)), (1, (8, 4)), (2, (5, 7)),
			(1, (8, 6)), (2, (5, 6)), (1, (8, 3)), (2, (4, 7)), (1, (3, 8))]
	b = board(15)
	for l in lst:
		b.place(l)
	print(b)
	new_state = state(2, 15, tmp_dict, (1,(3,8)), 0)
	new_state.set_children(new_state.successors())
	for child in new_state.get_children():
		print(child)
