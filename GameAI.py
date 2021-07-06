#!/usr/bin/env python

"""GameAI.py: INF1771 GameAI File - Where Decisions are made."""
"""
#############################################################
Copyright 2020 Augusto Baffa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#############################################################

__author__      = "Augusto Baffa"
__copyright__   = "Copyright 2020, Rio de janeiro, Brazil"
__license__ = "GPL"
__version__ = "1.0.0"
__email__ = "abaffa@inf.puc-rio.br"
#############################################################
"""
from MappingAI import *
import random
import re
from Map.Position import Position
from AstarS_AI import *


# <summary>
# Game AI Example
# </summary>
class GameAI():
    flag_fuga = False
    DecisionLis = []
    prevplayer = Position()
    player = Position()
    state = "ready"
    dir = "north"
    score = 0
    energy = 0
    mapp = Graph()
    visited = {}
    input = open("MapDiscovered.txt", 'r')
    virtualMap = []
    atacar = False
    estadoAtual = "explorar"
    fuga = False
    oldPos = ()
    countstep = 0
    fstpos = Position()
    fstposbool = True
    lastMove = ""
    for l in input:
        virtualMap.append(list(l))

    # <summary>
    # Refresh player status
    # </summary>
    # <param name="x">player position x</param>
    # <param name="y">player position y</param>
    # <param name="dir">player direction</param>
    # <param name="state">player state</param>
    # <param name="score">player score</param>
    # <param name="energy">player energy</param>
    def SetStatus(self, x, y, dir, state, score, energy):
        if (self.player.x != x or self.player.y != y) :
            self.prevplayer.x, self.prevplayer.y = self.player.x, self.player.y
        self.player.x = x
        self.player.y = y
        if (self.player.x, self.player.y) not in self.mapp.edges:
            self.mapp.edges[(self.player.x, self.player.y)] = {}
        if self.fstposbool:
            self.fstpos.x, self.fstpos.y = self.player.x, self.player.y
            self.fstposbool = False


        self.dir = dir.lower()

        self.state = state
        self.score = score
        self.energy = energy


    # <summary>
    # Get list of observable adjacent positions
    # </summary>
    # <returns>List of observable adjacent positions</returns>
    def GetObservableAdjacentPositions(self):
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y))
        ret.append(Position(self.player.x + 1, self.player.y))
        ret.append(Position(self.player.x, self.player.y - 1))
        ret.append(Position(self.player.x, self.player.y + 1))

        return ret


    # <summary>
    # Get list of all adjacent positions (including diagonal)
    # </summary>
    # <returns>List of all adjacent positions (including diagonal)</returns>
    def GetAllAdjacentPositions(self):
    
        ret = []

        ret.append(Position(self.player.x - 1, self.player.y - 1)) #0
        ret.append(Position(self.player.x, self.player.y - 1))     #1
        ret.append(Position(self.player.x + 1, self.player.y - 1)) #2

        ret.append(Position(self.player.x - 1, self.player.y))     #3(mais a esquerda do mapa)
        ret.append(Position(self.player.x + 1, self.player.y))     #4(mais a direita do mapa)

        ret.append(Position(self.player.x - 1, self.player.y + 1)) #5
        ret.append(Position(self.player.x, self.player.y + 1))     #6
        ret.append(Position(self.player.x + 1, self.player.y + 1)) #7

        return ret
    

    # <summary>
    # Get next forward position
    # </summary>
    # <returns>next forward position</returns>
    def NextPosition(self):
    
        ret = None
        
        if self.dir == "north":
            ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x + 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x - 1, self.player.y)

        return ret


    # <summary>
    # Player position
    # </summary>
    # <returns>player position</returns>
    def GetPlayerPosition(self):
        return self.player


    # <summary>
    # Set player position
    # </summary>
    # <param name="x">x position</param>
    # <param name="y">y position</param>
    def SetPlayerPosition(self, x, y):
        self.player.x = x
        self.player.y = y


    def random_virar(self):
        return random.choice(["virar_direita", "virar_esquerda"])

    def random_blocked(self):
        decision = self.random_virar()
        return [decision, "andar"]

    def insere_percurso(self, acao):
        if(len(self.DecisionLis) > 10):
            self.DecisionLis = acao
        else:
            self.DecisionLis = acao + self.DecisionLis

    def maquina_estado(self):
        estado = self.estadoAtual
        virar = self.random_virar()
        if estado == "atacar":
            self.DecisionLis = ["atacar"] + self.DecisionLis
        elif estado == "fugir" and self.flag_fuga == False:
            self.flag_fuga = True
            decision = ["andar",  virar, "andar", virar, "andar"]
            # melhorar depois
            self.DecisionLis = decision + self.DecisionLis

            # self.insere_percurso(decision)
        elif estado == "achou_ouro":
            self.DecisionLis = [ "pegar_anel"] + self.DecisionLis

            # self.insere_percurso(["pegar_ouro", "pegar_anel"])
        elif estado == "achou_powerUp":
            self.DecisionLis = ["pegar_powerup"] + self.DecisionLis

        elif estado == "breeze" or estado == "flash":
            if(self.lastMove == "andar_re"):
                self.DecisionLis = ["andar", "andar", random.choice(["virar_direita", "virar_esquerda"]), "andar_re"]
            else:
                self.DecisionLis = ["andar_re", "andar_re", random.choice(["virar_direita", "virar_esquerda"]), "andar"]

        elif estado == "explorar":
            self.flag_fuga = False
            if len(self.DecisionLis) == 0:
                self.DecisionLis = ["andar", "andar", random.choice(["virar_esquerda", "virar_direita", "andar"]), "andar", "andar"]

        elif estado == "steps":
            self.DecisionLis = ["andar_re", random.choice(["virar_direita", "virar_esquerda"]), "andar"] + self.DecisionLis
        
        elif estado == "blocked":
            if(self.lastMove == "virar_direita"):
                self.DecisionLis = ["virar_esquerda", "andar"] + self.DecisionLis
            elif(self.lastMove == "virar_esquerda"):
                self.DecisionLis = ["virar_direita", "andar"] + self.DecisionLis
            else:
                self.DecisionLis = [random.choice(["virar_direita", "virar_esquerda"]), "andar"] + self.DecisionLis

        # elif estado == "random":
        #     self.DecisionLis = [random.choice(["virar_direita", "virar_esquerda"]), "andar"]

    def ValidPos(self, x, y): #  59 x 34
        return (x <= 59 and x >= 0) and (y <= 34 and y >= 0)

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):
        #cmd = "";
        # for s in o:
        # enemy = s.split('#')
        self.countstep += 1
        print("count  ", self.countstep)

        astar = []
        constsofar = {}
        if self.countstep >= 10:
            astar, costsofar = a_star_search(self.mapp, (self.player.x, self.player.y), (self.fstpos.x, self.fstpos.y))
            self.countstep = 0
            n = pathFinder((self.fstpos.x, self.fstpos.y), (self.player.x, self.player.y), astar)
            print("inicio ",(self.fstpos.x, self.fstpos.y), len(n), n)
            # move_to_star = self.GetPlayerPosition
            # print("AStar -> ", "inicio ",(self.fstpos.x, self.fstpos.y), astar)
            # print(pathFinder((self.player.x, self.player.y), (self.fstpos.x, self.fstpos.y), astar))
        
        if "blocked" in o:

            self.estadoAtual = "blocked"
            self.maquina_estado()
            npos = self.NextPosition()
            pos = self.GetPlayerPosition()
            ppos = self.prevplayer

            self.mapp.edges[(pos.x, pos.y)][(npos.x, npos.y)] = Obstacle(1000, 'O', "none", 1)
            self.virtualMap[npos.y][npos.x] = self.mapp.edges[(pos.x, pos.y)][(npos.x, npos.y)].getsign()

            self.mapp.edges[(pos.x, pos.y)][(ppos.x, ppos.y)] = Obstacle(1, '.', "none", 1)


        for i in o:
            if "enemy" in i:
                enemy = i.split('#')
                enemyDist = int(enemy[1])
                if(enemyDist < 15 and self.energy > 50):
                    self.estadoAtual = "atacar"
                else:
                    self.estadoAtual = "fugir"
                self.maquina_estado()

        if "damage" in o:

            self.estadoAtual = "fugir"
            self.maquina_estado()

        if "steps" in o:
            self.estadoAtual = "steps"
            self.maquina_estado()
            pass

        if "breeze" in o:

            self.estadoAtual = "breeze"
            self.maquina_estado()

            pos = self.GetPlayerPosition()
            ppos = self.prevplayer
            npos = self.NextPosition()
            allpos = []

            self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(1, '.', "none", 1)
            self.mapp.edges[(pos.x, pos.y)][(ppos.x, ppos.y)] = Obstacle(1, '.', "none", 1)

            allpos = self.GetAllAdjacentPositions()
            loc3 = [(npos.x, npos.y), (allpos[3].x, allpos[3].y), (allpos[4].x, allpos[4].y)]
            for i in loc3:
                if i not in self.mapp.edges[(pos.x, pos.y)]:
                    self.mapp.edges[(pos.x, pos.y)][i] = None
                if type(self.mapp.edges[(pos.x, pos.y)][i]) != Obstacle:
                    self.mapp.edges[(pos.x, pos.y)][i] = Obstacle(1000, 'x', "Buraco", 0.25)
                self.virtualMap[i[1]][i[0]] = self.mapp.edges[(pos.x, pos.y)][i].getsign()
            

        if "flash" in o:

            self.estadoAtual = "flash"
            self.maquina_estado()

            pos = self.GetPlayerPosition()
            ppos = self.prevplayer
            npos = self.NextPosition()
            allpos = []

            self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(1, '.', "none", 1)
            self.mapp.edges[(pos.x, pos.y)][(ppos.x, ppos.y)] = Obstacle(1, '.', "none", 1)

            allpos = self.GetAllAdjacentPositions()
            loc3 = [(npos.x, npos.y), (allpos[3].x, allpos[3].y), (allpos[4].x, allpos[4].y)]

            for i in loc3:
                if i not in self.mapp.edges[(pos.x, pos.y)]:
                    self.mapp.edges[(pos.x, pos.y)][i] = None
                if type(self.mapp.edges[(pos.x, pos.y)][i]) != Obstacle:
                    self.mapp.edges[(pos.x, pos.y)][i] = Obstacle(1000, 't', "Teleport", 0.25)
                self.virtualMap[i[1]][i[0]] = self.mapp.edges[(pos.x, pos.y)][i].getsign()


        if "blueLight" in o:

            self.estadoAtual= "achou_powerUp"
            self.maquina_estado()

            pos = self.GetPlayerPosition()
            ppos = self.prevplayer

            self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(0.5, 'E', "energy", 1)
            self.mapp.edges[(pos.x, pos.y)][(ppos.x, ppos.y)] = Obstacle(1, '.', "none", 1)

            self.virtualMap[pos.y][pos.x] = self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)].getsign()
            print("POS POWER X:", str(pos.x),"Y" ,str(pos.y))
           

        if "redLight" in o:

            self.estadoAtual= "achou_ouro"
            self.maquina_estado()
            pos = self.GetPlayerPosition()
            ppos = self.prevplayer

            self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(0.5, 'G', "gold", 1)
            self.mapp.edges[(pos.x, pos.y)][(ppos.x, ppos.y)] = Obstacle(1, '.', "none", 1)

            self.virtualMap[pos.y][pos.x] = self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)].getsign()

        # if len(self.DecisionLis) == 0:
        #     print("decision random")
        #     self.estadoAtual = "random"
        #     self.maquina_estado()

        print("obs", o)
        # for i in self.virtualMap:
        #     print(''.join(i))



    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):

        self.estadoAtual = "explorar"
        self.maquina_estado()
        pos = self.GetPlayerPosition()
        ppos = self.prevplayer
        self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(1, '.', "none", 1)
        self.mapp.edges[(pos.x, pos.y)][(ppos.x, ppos.y)] = Obstacle(1, '.', "none", 1)

        if self.virtualMap[pos.y][pos.x] not in "GExXtT":
            self.virtualMap[pos.y][pos.x] = self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)].getsign()
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    # "virar_direita" , "virar_esquerda" , "andar" , "atacar" , "pegar_ouro" , "pegar_anel" , "pegar_powerup" , "andar_re"
    def GetDecision(self):
        print("--> ", self.DecisionLis)
        if len(self.DecisionLis) > 0:
            self.lastMove = self.DecisionLis[0]
            return self.DecisionLis.pop(0)
        # print("decision random")
        # n = random.choice(["virar_direita", "virar_esquerda", "andar", "andar", "andar", "andar", "andar"])
        # self.lastMove = n
        # return n
