from player import *
from board import *

if __name__ == '__main__':

	while True:
		try:
			size = int(input('Of what size do you want the board to be?\n'))
			break
		except:
			print('Invalid input content!')

	board = board(size)
	players = [None, None]

	for i in range(2):
		while True:
			z = input('Who do you want to play ' + ('O' if i else 'X') + '? (AI/human)\n').lower()
			if z == 'ai':
				players[i] = AI(board, i + 1)
				player.AI_player += 1
				break
			elif z == 'human':
				players[i] = keyboard_player(board, i + 1)
				break
			print('Invalid input content!')

	while not players[0].play() and not players[1].play():
		pass

	print(board)
	print()
	print('GAME OVER')
