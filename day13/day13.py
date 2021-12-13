#!/usr/bin/python3
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day13.dat", "r").read().splitlines()


fold = False
P = set()
F = []

for line in lines:
  if line != "":
    if fold == False:
      x,y = [int(x) for x in line.split(",")]
      P.add((x,y))
    else:
      a,l = line.split("=")
      l = int(l)
      if "along x" in a:
        F.append(("x",l))
      else:
        F.append(("y",l))
  else:
    fold = True
    
for i,f in enumerate(F):
  a,l = f
  P2 = set()
  for p in P:
    x,y = p
    if a == "y":
      if y > l:
        y = l-abs(y-l)
    if a == "x":
      if x > l:
        x = l-abs(x-l)
    P2.add((x,y))
  P = P2.copy()
  if i == 0:
    print("Part1: ", len(P))

print("Part2:")  
minx = 10e9
miny = 10e9
maxx = -10e9
maxy = -10e9
for p in P:
  minx = min(minx, p[0])
  miny = min(miny, p[1])
  maxx = max(maxx, p[0])
  maxy = max(maxy, p[1])

for y in range(miny,maxy+1):
  tmp = ""
  for x in range(minx,maxx+1):
    if (x,y) in P:
      tmp += "#"
    else:
      tmp += " "
      
  print(tmp)
  
