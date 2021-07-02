from typing import TypeVar, List
import numpy as np
from AG import *

Location = TypeVar('Location')
Weight = TypeVar('Weight')

class Obstacle:
    def __init__(self, w, it):
        self.weight = w
        self.itemtype = it


class Graph:
    def __init__(self):
        self.edges: Dict[Location, {Location : obstacle}] = {}
    
    def neighbors(self, pos: Location) -> List[Location]:
        return list(self.edges[pos])

    #custo de movimento entre vizinhos
    def cost(self, from_pos: Location, to_pos: Location) -> float:
        return self.edges[from_pos][to_pos]


def getNeighborsTuples(pos: Location, Length: int, Heigth: int) -> List[Location]:
    lis = []
    if pos[0] <= Heigth - 2:
        lis.append((pos[0] + 1, pos[1]))
    if pos[0] >= 1:
        lis.append((pos[0] - 1, pos[1]))
    if pos[1] <= Length - 2:
        lis.append((pos[0], pos[1] + 1))
    if pos[1] >= 1:
        lis.append((pos[0], pos[1] - 1))
    return lis



def tileTograph(filetxt: str, symval: dict) -> Graph:
    f = open(filetxt, 'r+')
    graph = Graph()
    global inputt
    inputt = np.loadtxt(filetxt, dtype='str')
    for idxl, line in enumerate(inputt):
        for idxc, col in enumerate(line):
            neighbors = getNeighborsTuples((idxl, idxc), len(inputt[0]), len(inputt))
            auxdict = {}
            for ngbr in neighbors:
                auxdict[ngbr] = symval[inputt[ngbr[0]][ngbr[1]]]
            graph.edges[(idxl, idxc)] = auxdict
    return graph, inputt

def sortKey1(l):
    return l[-1]

def heuristic1(a, b):
    #Manahattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Reconstruct A* path
def pathFinder(goal: Location, came_from: dict):
    path = []
    current = goal
    while current != start: 
        path.append(current[::-1])
        current = came_from[current]
    return path

def a_star_search(graph: Graph, start: Location, goal: Location):
    frontier = []
    frontier.append((start, 0))
    came_from: Dict[Location, Optional[Location]] = {}
    cost_so_far: Dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    
    while len(frontier) != 0:
        frontier.sort(key=sortKey1)
        current = frontier[0][0]
        frontier.pop(0)
        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic1(next, goal)
                frontier.append((next, priority))
                came_from[next] = current

    return came_from, cost_so_far

# example_graph = Graph()
# example_graph.edges = {
#     'A': {'B': 10},
#     'B': {'C': 1},
#     'C': {'B': 3, 'D': 4, 'F': 8},
#     'D': {'C': 78, 'E': 90},
#     'E': {'F': 5},
#     'F': {},
# }
# pokes_gym = []
# start = (37, 36)
# goal = (4, 36)
# gymname = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C']
# symval = {'M' : 200, 'R' : 5, '.' : 1, 'F' : 0, 'I' : 0}

# #Gym associate to AG solution
# bestchromosome, qtdMutant = Poke_Genetic()
# for j in range(12):
#     aux = []
#     for i in bestchromosome.chromosome:
#         aux.append((i.subchromosome[j], i.power))
#     pokes_gym.append(aux)

# print(pokes_gym)
# for i in range(1,13):
#     symval[gymname[i-1]] = round(GymDificulty[i-1] / ((pokes_gym[i-1][0][0]*pokes_gym[i-1][0][1] +
#     pokes_gym[i-1][1][0]*pokes_gym[i-1][1][1] + 
#     pokes_gym[i-1][2][0]*pokes_gym[i-1][2][1] + 
#     pokes_gym[i-1][3][0]*pokes_gym[i-1][3][1] + 
#     pokes_gym[i-1][4][0]*pokes_gym[i-1][4][1]) or 1), 1)
# print(symval)

# g = Graph()
# g, m = tileTograph('tile.txt', symval)
# came_from, cost_so_far = a_star_search(g, start, goal)
# print(cost_so_far[(38,20)])
# pathf = pathFinder(goal, came_from)