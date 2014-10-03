from heapq import heappush, heappop # for priority queue
import math
import time
import Queue
from Tkinter import *


class node:
    xPos = 0 # x position
    yPos = 0 # y position
    cost = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate
    algorithm = 0

    def __init__(self, xPos, yPos, cost, priority,the_map, algorithm):
        self.xPos = xPos
        self.yPos = yPos
        self.priority = priority
        if algorithm == '1':
            self.cost += 0
        else:
            self.cost += cost
            self.getCost(the_map)
        self.algorithm = algorithm
        print self.algorithm

    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority

    def updatePriority(self, xDest, yDest):
        if self.algorithm == '0' or self.algorithm == '1':
            self.priority = self.cost + self.hFunction(xDest, yDest) # A*
        if self.algorithm == '2':
            self.priority = self.cost

    def getCost(self, the_map):
        next_node_type = the_map[self.yPos][self.xPos]
        if self.algorithm == '1':
            self.cost += 1
        elif next_node_type == "w":
            self.cost += 100
        elif next_node_type == "m":
            self.cost += 50
        elif next_node_type == "f":
            self.cost += 10
        elif next_node_type == "g":
            self.cost += 5
        elif next_node_type == "r":
            self.cost += 1
        elif next_node_type == "#":
            self.cost += 10000

    # Estimate remaining distance to the goal.
    def hFunction(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = abs(xd) + abs(yd)
        return(d)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKGREY= '\x1b[30m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    RED = '\x1b[31;1m'
    GREEN = '\x1b[36;1m'


# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB, algorithm):
    print algorithm
    closed_nodes_map = [] # map of closed (tried-out) nodes
    open_nodes_map = [] # map of open (not-yet-tried) nodes
    dir_map = [] # map of dirs
    row = [0] * n
    for i in range(m): # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0,the_map, algorithm)
    n0.updatePriority(xB, yB)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.cost, n1.priority,the_map,algorithm)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[y][x] = 0
        closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

        # stop searching if we have reached the goal and generate the path
        if x == xB and y == yB:
            path = ''
            while not (x == xA and y == yA):
                j = dir_map[y][x]
                c = str((j + 2) % 4)
                path = c + path
                x += dx[j]
                y += dy[j]
            return path, closed_nodes_map, open_nodes_map

        # generate moves (child nodes) in all possible dirs
        for i in range(4):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1 or closed_nodes_map[ydy][xdx] == 1 or the_map[ydy][xdx] == '#'):
                # generate a child node
                m0 = node(xdx, ydy, n0.cost, n0.priority,the_map, algorithm)
                m0.updatePriority(xB, yB)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found



def chooseAlgo():
    algorithm = raw_input("Choose an algorithm: 0: AStar, 1: BFS, 2: Dijkstra: ")

    if algorithm == '0' or algorithm == '1' or algorithm == '2':
        return algorithm
    else:
        print "Wrong input, try again"
        chooseAlgo()

def main():
    dirs = 4 # number of possible directions to move on the map
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    y = 0
    x = 0
    xA = 0
    yA = 0
    xB = 0
    yB = 0

    array = []

    #allows user to choose what map to use and adds the board to a array
    algorithm = chooseAlgo()
    print algorithm
    map = raw_input("Choose a map between 1-4, or 21-24: ")
    board = open(map+".txt","r").readlines()
    for line in board:
        x = 0
        preArray = []
        for char in line:
            if char == 'A':
                xA = x
                yA = y
                preArray.append('A')
            elif char == 'B':
                xB = x
                yB = y
                preArray.append('B')
            elif char == '.':
                preArray.append('r')
            elif char == '#':
                preArray.append('#')
            elif char != '\n':
                preArray.append(char)
            x += 1
        y += 1
        array.append(preArray)


    n = x-1 # horizontal size of the map
    m = y # vertical size of the map

    print '-----------------------------------------------------------'
    print 'Information: '
    print ' '
    print 'Map size (X,Y): ', n, m
    print 'Start: ', xA, yA
    print 'Finish: ', xB, yB
    t = time.time()
    print algorithm
    route, closed_nodes, open_nodes = pathFind(array, n, m, dirs, dx, dy, xA, yA, xB, yB,algorithm)
    print closed_nodes
    print open_nodes
    print 'Time to generate the route (seconds): ', time.time() - t
    print 'Route: ' + route
    

    # mark the route on the map
    if len(route) > 0:
        x = xA
        y = yA
        array[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            array[y][x] = array[y][x].upper()
        array[y][x] = 4

    #The visualization of the map
    print '-----------------------------------------------------------'
    print 'Map:'
    print ' '
    for y in range(m):
        for x in range(n):
            xy = array[y][x]
            if isinstance(xy,str) and xy.isupper():
                print bcolors.RED + xy + bcolors.ENDC,  # route
            elif xy == 2:
                print bcolors.RED + 'A' + bcolors.ENDC,
            elif xy == 4:
                print bcolors.RED + 'B' + bcolors.ENDC,
            elif xy == 'm':
                if closed_nodes[y][x] == 1:
                    print bcolors.OKGREY + 'x' + bcolors.ENDC,
                elif open_nodes[y][x] != 0:
                    print bcolors.OKGREY + '*' + bcolors.ENDC,
                else:
                    print bcolors.OKGREY + xy + bcolors.ENDC,
            elif xy == 'w':
                if closed_nodes[y][x] == 1:
                    print bcolors.OKBLUE + 'x' + bcolors.ENDC,
                elif open_nodes[y][x] != 0:
                    print bcolors.OKBLUE + '*' + bcolors.ENDC,
                else:
                     print bcolors.OKBLUE + xy + bcolors.ENDC,
            elif xy == 'r':
                if closed_nodes[y][x] == 1:
                    print bcolors.WARNING + 'x' + bcolors.ENDC,
                elif open_nodes[y][x] != 0:
                    print bcolors.WARNING + '*' + bcolors.ENDC,
                else:
                    print bcolors.WARNING + xy + bcolors.ENDC,
            elif xy == 'g':
                if closed_nodes[y][x] == 1:
                    print bcolors.OKGREEN + 'x' + bcolors.ENDC,
                elif open_nodes[y][x] != 0:
                    print bcolors.OKGREEN + '*' + bcolors.ENDC,
                else:
                    print bcolors.OKGREEN + xy + bcolors.ENDC,
            elif xy == 'f':
                if closed_nodes[y][x] == 1:
                    print bcolors.GREEN + 'x' + bcolors.ENDC,
                elif open_nodes[y][x] != 0:
                    print bcolors.GREEN + '*' + bcolors.ENDC,
                else:
                    print bcolors.GREEN + xy + bcolors.ENDC,
            else:
                print bcolors.WARNING + xy + bcolors.ENDC, # finish

        print


main()