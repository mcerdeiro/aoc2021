#!/usr/bin/python3
import copy
from typing import List

lines = open("day09.dat", "r").read().splitlines()

D = {}

def getNei(x,y):
  ret = []
  ret.append((x-1,y)) if x > 0 else 0
  ret.append((x, y-1)) if y > 0 else 0
  ret.append((x+1, y)) if x < len(lines[0])-1 else 0
  ret.append((x,y+1)) if y < len(lines)-1 else 0
  return ret

def getSize(x,y):
  C = set()
  C.add((x,y))
  TOC = set(getNei(x,y))
  while len(TOC) != 0:
    v = TOC.pop()
    if D[(v[0], v[1])] != 9:
      C.add(v)
      newNew = getNei(v[0],v[1])
      for n in newNew:
        if n not in C and n not in TOC:
          TOC.add(n)
  return(len(C))

def checkMin(x,y):
  mini = True
  nei = getNei(x,y)
  for n in nei:
    if D[n] <= D[(x,y)]:
      mini = False
  return mini

for i in range(len(lines)):
  for j in range(len(lines[i])):
    D[(j,i)] = int(lines[i][j])

L = []

p1 = 0 
for i in range(len(lines)):
  for j in range(len(lines[0])):
    if checkMin(j,i):
      p1 += D[(j,i)]+1
      L.append((j,i)) 
    

print("Part1:", p1)
S = []
for l in L:
  size = getSize(l[0], l[1])
  S.append(size)

S.sort()
print("Part2:", S[-1]*S[-2]*S[-3])
