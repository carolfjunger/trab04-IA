from typing import TypeVar, List
from MappingAI import *

Location = TypeVar('Location')


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