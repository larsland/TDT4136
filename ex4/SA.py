__author__ = 'trulsmp & larsland'
import math
import numpy as np
import random
import time
from random import randint, shuffle, randrange

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

#Takes inn the size of the board, and maximum number of eggs in a row/col/diagonal from the user
m = n = int(input("M and N value: "))
k = int(input("K value: "))

#Initiating a timer
startTime = time.time()

#The optimal number of eggs that can be placed on the board.
max_eggs = m*k

#Method for calculating the numbe rof eggs placed on the board
def calculate_score(board):
    score = 0
    for i in range(0,m):
        for j in range(0,n):
            if board[i][j] == '1':
                score += 1
    return score

#Method for printing the board as a nice string
def print_board(board):
    string = ''
    for i in range(0,m):
        string += '|'
        for j in range(0,n):
            if board[i][j] == "0":
                string += bcolors.YELLOW + " - " + bcolors.ENDC
            else: 
                string += bcolors.GREEN + " O " + bcolors.ENDC
        string += '|\n'
    print(string)

#Returns a 2d array with only '0's.
def initiate_board():
    board = []
    for i in range(0,m):
        board.append([])
        for j in range(0,n):
            board[i].append('0')
    return board


def generate_start(board):
    '''
    Takes the initial board, and places 'eggs' randomly on each row
    of the board, while keeping the eggs to be less or equal to than the k-vlaue
    in each row
    '''
    eggs = max_eggs
    while eggs > 0:
        for i in range(n):
            x = randint(0,n-1)
            board[i][x] = '1'
            eggs -= 1
            putted = 1
            while putted < k:
                y = randint(0,n-1)
                if board[i][x] != board[i][y]:
                    board[i][y] = '1'
                    eggs -= 1
                    putted += 1

    return board


#Checks if the given board follows all the rules, and then calculates the score for it
def objective(board):
    if validateBoard(board):
        return calculate_score(board)
    else:
        return 1;


def evaluate_neighbours(neighbours):
    '''
    Finds the best of the neighbours produced in the generate_neighbours 
    method, based on its score and validness, then returns it.
    '''
    highest_neighbour = neighbours[0]
    for i in neighbours:
        if objective(i) > objective(highest_neighbour):
            highest_neighbour = i
    return highest_neighbour

def generate_neighbours(board):
    '''
    Generates a set of neighbours (new boards) out of the initial given board.
    '''
    to_check = []
    cols = []
    rows = []

    # Finds all columns
    for i in range (len(board)):
        temp = []
        for j in range(len(board)):
            temp.append(board[j][i])
        cols.append(temp)

    # All columns with number of eggs > k, appended to a list
    to_check = [row for row in cols if row.count('1') > k ]

    # Finding all rows that has an egg in a column > k eggs, and adds it to rows.
    rows = []

    for row in to_check:
        for x in range(len(row)):
            if row[x] == '1' and board[x] not in rows:
                rows.append(board[x])

    neighbours = []
    for x in range(len(board)):
        if board[x] in rows:
            boardcopy = list(board)
            row = board[x]
            row = list(row)
            shuffle(row)
            board[x] = row
            neighbours.append(board)
            board = boardcopy


    '''
    This method doesn't handle situations with more than k eggs in
    the diaglonals, so instead it shuffles the first row of the board
    till the diagonals are fine.
    '''

    if len(neighbours) == 0:
        neighbour = list(board)
        row = board[0]
        row = list(row)
        shuffle(row)
        neighbour[0] = row
        return [neighbour]
    return neighbours



#Returns True if the board has no more than 2 eggs in each row, False otherwise
def checkRow(board):
    count = 0
    for i in range(n):
        count = 0
        for x in range(m):
            if (board[i][x] == '1'):
                    count += 1
        #print count
        if count > k:
            return False
    return True

#Returns True if the board has no more than 2 eggs in each collumn, False otherwise
def checkCol(board):
    count = 0
    for i in range(n):
        count = 0
        for x in range(m):
            if (board[x][i] == '1'):
                    count += 1
        #print count
        if count > k:
            return False
    return True

#Returns True if the board has no more than 2 eggs in each diagonal, False otherwise
def checkDiagonal(board):
    '''
    We use a module called numpy array to solve the diagonal check
    '''
    # create a numpy array
    a = np.array(board)
    # Then a list comprehension is used to collect all the diagonals
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]

    # Now back to the original array to get the upper-left-to-lower-right diagonals,
    # starting from the right, so the range needed for shape (x,y) was y-1 to -x+1 descending.
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))

    # Another list comp to convert back to Python lists from numpy arrays
    diagonals = [n.tolist() for n in diags]
    eggs = 0
    for i in diagonals:
        for y in i:
            if y == '1':
                eggs += 1
        if eggs > k:
            return False
        eggs = 0

    return True
    
#Help method for checking all the check-methods, to see if the given board is valid
def validateBoard(board):
    if checkRow(board) and checkCol(board) and checkDiagonal(board):
        return True
    else:
        return False

#The main algorithm
def SA():
    temperature = 1000000  # ???

    board = initiate_board()
    board = generate_start(board)
    max_board = board

    F = objective(board)  # Objective function
    
    while temperature > 0:
    
        neighbours = generate_neighbours(board)
        p_max = evaluate_neighbours(neighbours)
        if objective(max_board) < objective(p_max):
            max_board = p_max
        if objective(board) == max_eggs:
            return board
        q = (objective(p_max) - (objective(board)/objective(board)))
    
        p = min(1, math.e**(-q/temperature))
    
        x = random.randint(0,1)
        if x > p:
            board = p_max
        else:
            board = random.choice(neighbours)
    
        temperature -= 0.04

    return max_board



final_board = SA()

#Printing the final solution, validation and elapsed time
print""
print"Board:"
print" "
print_board(final_board)
print "Valid board:",validateBoard(final_board)
elapsedTime = time.time() - startTime
print "Elapsed time:","{0:.4f}".format(elapsedTime),"seconds"



#Class holding colors for console printing
class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

