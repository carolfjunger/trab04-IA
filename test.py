import numpy as np
from MappingAI import *


asd = Graph()
asd.a = (1,2)
asd.edges[(1,1)][(1,3)] = 33
# print(type(asd.edges[0][0]))

input = open("MapDiscovered.txt", "r")
# type(input[10][0][10]) = '.'
# lis = []
# for l in input:
#     lis.append([l])
# aux = list(lis[2][0])
# aux[4] = "."
# lis[2] = ["".join(aux)]
# for i in lis:
#     print(i)