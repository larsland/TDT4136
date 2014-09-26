
def checkBoard():
	board = open("boards/board-1-1.txt","r").read()
	for line in board:
		for char in line:
			if char == '.':
				print ("This node is walkable")
			elif char == '#':
				print("This node is a wall")
			elif char == 'A':
				print("This is where you start")
			elif char == 'B':
				print("This is your destination!")

def main():
	checkBoard()
	
main()