#!/usr/bin/python3
import copy
from typing import List
import sys

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day11.dat", "r").read().splitlines()

O = {}

def getNei(x,y):
  nei = []
  nei.append((x-1,y)) if x > 0 else 0
  nei.append((x,y-1)) if y > 0 else 0
  nei.append((x+1,y)) if x < len(lines[0])-1 else 0
  nei.append((x,y+1)) if y < len(lines)-1 else 0
  nei.append((x-1,y-1)) if x > 0 and y > 0 else 0
  nei.append((x+1,y+1)) if x < len(lines[0])-1 and y < len(lines)-1 else 0
  nei.append((x+1,y-1)) if x < len(lines[0])-1 and y > 0 else 0
  nei.append((x-1,y+1)) if x > 0 and y < len(lines)-1 else 0
  return nei


for i in range(len(lines)):
  for j in range(len(lines[i])):
    O[(j,i)] = int(lines[i][j])
  
O2 = {}  
p1 = 0
for i in range(100000):
  for x in range(len(lines[0])):
    for y in range(len(lines)):
      O2[(x,y)] = O[(x,y)] + 1
  
  O = O2
  F = set()
  for x in range(len(lines[0])):
    for y in range(len(lines)):
      
      TOINC = []
      if O[(x,y)] > 9:
        if (x,y) not in F:
          F.add((x,y))
          p1 += 1
          TOINC = getNei(x,y)
          while len(TOINC):
            p = TOINC.pop()
            O[p] += 1
            if O[p] > 9 and p not in F:
              F.add(p)
              p1 += 1
              TOINC += getNei(p[0],p[1])

  for p in F:
    O[p] = 0
    
  if i == 99:
    print("Part 1:", p1)
  if (len(F) == 100):
    print("Part 2:", i+1)
    exit()
