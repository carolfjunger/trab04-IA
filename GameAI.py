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
from Map.Position import Position

# <summary>
# Game AI Example
# </summary>
class GameAI():

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
    percurso = []
    oldPos = ()
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
        if(self.player.x != x or self.player.y != y ):
            self.oldPos = (self.player.x , self.player.y )
        self.player.x = x
        self.player.y = y
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
    # Get previous position, once it walked forward
    # </summary>
    # <returns>previous backward position</returns>
    def PrevPosition(self):

        
        ret = None

        if self.dir == "north":
            ret = Position(self.player.x, self.player.y + 1)
                
        elif self.dir == "east":
                ret = Position(self.player.x - 1, self.player.y)
                
        elif self.dir == "south":
                ret = Position(self.player.x, self.player.y - 1)
                
        elif self.dir == "west":
                ret = Position(self.player.x + 1, self.player.y)

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

    def insere_percurso(self, acao):
        self.percurso.insert(0, acao)

    def maquina_estado(self):
        estado = self.estadoAtual

        if(estado == "atacar"):
            self.insere_percurso("atacar")
        elif (estado == "fugir"):
            # melhorar depois
            self.insere_percurso("virar_esquerda")
            self.insere_percurso("andar")
            self.insere_percurso("virar_esquerda")
            self.insere_percurso("andar")
            self.insere_percurso("virar_esquerda")
            self.insere_percurso("andar")
        elif (estado == "achou_ouro"):
            self.insere_percurso("pegar_ouro")
        elif (estado == "achou_powerUp"):
            pos = self.GetPlayerPosition()
            print("PEGOU POWER X:", str(pos.x),"Y" ,str(pos.y))
            self.insere_percurso("pegar_powerup")

            

    # <summary>
    # Observations received
    # </summary>
    # <param name="o">list of observations</param>
    def GetObservations(self, o):
        print('oldPos', self.oldPos)
        pos = self.GetPlayerPosition()
        print('pos', (pos.x, pos.y))
        #cmd = "";
        for s in o:
            enemy = s.split('#')
            

            if s == "blocked":
                npos = self.NextPosition()
                pos = self.GetPlayerPosition()
                # self.visited[(npos.x, npos.y)] = Obstacle(1000, 'O', "none")
                if (pos.x, pos.y) not in self.mapp:
                    self.mapp[(pos.x, pos.y)] = {}
                self.mapp.edges[(pos.x, pos.y)][(npos.x, npos.y)] = Obstacle(1000, 'O', "none")
                self.virtualMap[npos.y][npos.x] = "O"
                self.estadoAtual= ""

            elif s == "steps":

                self.estadoAtual= ""
                pass
            
            elif s == "breeze":

                self.estadoAtual= ""
                pass

            elif s == "flash":
                pos = self.GetPlayerPosition()
                ppos = self.PrevPosition()
                # if ()
                # self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(0.5, 'T', "Teleporter")
                self.virtualMap[pos.y][pos.x] = "T"
                self.estadoAtual= ""
            elif s == "blueLight":
                pos = self.GetPlayerPosition()
                ppos = self.PrevPosition()
                # self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(0.5, 'G', "gold")
                self.virtualMap[pos.y][pos.x] = "E"
                print("POS POWER X:", str(pos.x),"Y" ,str(pos.y))
                self.estadoAtual= "achou_powerUp"
            elif s == "redLight":
                pos = self.GetPlayerPosition()
                ppos = self.PrevPosition()
                # self.mapp.edges[(ppos.x, ppos.y)][(pos.x, pos.y)] = Obstacle(0.5, 'G', "gold")
                self.virtualMap[pos.y][pos.x] = "G"
                self.estadoAtual= "achou_ouro"
            elif enemy[0] == "enemy":
                enemyDist = int(enemy[1])
                if(enemyDist < 7):
                    self.estadoAtual = "atacar"
                else:
                    self.estadoAtual= ""
                    print("SEGUE")
            elif s == "damage":
                self.estadoAtual = "fugir"
            elif s == '':
                self.estadoAtual= ""

            self.maquina_estado()

        print("obs", o)
        # print(self.virtualMap[0][0])
        for i in self.virtualMap:
            print(''.join(i))





    # <summary>
    # No observations received
    # </summary>
    def GetObservationsClean(self):
        pos = self.GetPlayerPosition()
        ppos = self.PrevPosition()
        # self.mapp.edges[(ppos.x, ppos.y)][pos.x, pos.y] = Obstacle(1, '.', "none")
        self.virtualMap[pos.y][pos.x] = "."
    

    # <summary>
    # Get Decision
    # </summary>
    # <returns>command string to new decision</returns>
    # "virar_direita" , "virar_esquerda" , "andar" , "atacar" , "pegar_ouro" , "pegar_anel" , "pegar_powerup" , "andar_re"
    def GetDecision(self):
        

        x = self.GetPlayerPosition().x
        y = self.GetPlayerPosition().y
        print(x , y)
        # for i in self.GetAllAdjacentPositions():
        #     print(i.x, i.y)

        if(len(self.percurso)):
            comando = self.percurso.pop(0)
            if(comando == 'atacar'):
                print("ATIROU")
            return comando
        
        n = random.randint(0,6)

        

        if n == 0:
            return "virar_direita"
        elif n == 1:
            return "virar_esquerda"
        elif n == 2:
            return "andar"
        elif n == 3:
            return "andar"
        elif n == 4:
            return "andar"
        elif n == 5:
            return "andar"
        elif n == 6:
            return "andar"
        elif n == 7:
            print("ATIROU")
            return "atacar"

        return ""