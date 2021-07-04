from typing import TypeVar, List
import numpy as np

Location = TypeVar('Location')

class Obstacle:
    def __init__(self, w, ch, it, c):
        self.weight = w
        self.itemtype = it
        self.chance = c
        self.character = ch

    def getsign(self):
        if self.chance >= 1:
            return self.character.upper()
        else:
            return self.character
    def setarea(self, c):
        self.chance += c
        if self.chance >= 1:
            self.character = self.character.upper()

    def getweight(self):
        return self.weight


class Graph:
    def __init__(self):
        #{location : {lcation : Obstacle}}
        self.edges = {}
        self.a = (int,int)
    def neighbors(self, pos: Location) -> List[Location]:
        return list(self.edges[pos])

    #custo de movimento entre vizinhos
    def cost(self, from_pos: Location, to_pos: Location) -> float:
        return self.edges[from_pos][to_pos].getweight()
