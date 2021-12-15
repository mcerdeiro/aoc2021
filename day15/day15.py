#!/usr/bin/python3
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day15.dat", "r").read().splitlines()

M = {}
X = 0
Y = 0

for y in range(len(lines)):
  for x in range(len(lines[y])):
    M[(x,y)] = int(lines[y][x])
    X = max(X, x+1)
    Y = max(Y, y+1)

def getNei(p):
  ret = []
  ret.append((p[0]-1,p[1])) if p[0] > 0 else 0
  ret.append((p[0],p[1]-1)) if p[1] > 0 else 0
  ret.append((p[0]+1,p[1])) if p[0] < X-1 else 0
  ret.append((p[0],p[1]+1)) if p[1] < Y-1 else 0
  return ret
    
def solve():
  pos = (0,0)
  price = 0

  V = {pos: 0}
  tovisit = getNei(pos)
  TOVISIT = []
  for tv in tovisit:
    TOVISIT.append((M[tv], tv))
  

  while (X-1,Y-1) not in V:
    current = heapq.heappop(TOVISIT)
    newMin = False
    if current[1] not in V:
      V[current[1]] = current[0]
      newMin = True
    else:
      if current[0] < V[current[1]]:
        V[current[1]] = current[0]
        newMin = True

    if newMin:
      tovisit = getNei(current[1])
      for tv in tovisit:
        heapq.heappush(TOVISIT, (V[current[1]]+M[tv], tv))
            
  return V[(X-1,Y-1)]
    

print("Part1", solve())
for muly in range(5):
  for mulx in range(5):
    for y in range(X):
      for x in range(Y):
        if mulx > 0 or muly > 0:
          newv = (M[(x,y)] + mulx + muly)
          if newv > 9:
            newv -= 9
          M[(x+mulx*X,y+muly*Y)] = newv
  
X = X*5
Y = Y*5
print("Part2", solve())

