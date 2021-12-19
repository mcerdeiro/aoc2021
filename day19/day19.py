#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day19.dat", "r").read().splitlines()

S = []
nextScanner = None

def rotations(bacon):
  XA = [(1, 1, 1, 1), (0, 0, 0, 0), (0, 0, 0, 0)]
  YA = [(0, 0, 0, 0), (1, 0, -1, 0), (0, -1, 0, 1)]
  ZA = [(0, 0, 0, 0), (0, 1, 0, -1), (1, 0, -1, 0)]
  R = []
  for xa in range(4):
    x = XA[0][xa] * bacon[0] + XA[1][xa] * bacon[1] + XA[2][xa] * bacon[2]
    y = YA[0][xa] * bacon[0] + YA[1][xa] * bacon[1] + YA[2][xa] * bacon[2]
    z = ZA[0][xa] * bacon[0] + ZA[1][xa] * bacon[1] + ZA[2][xa] * bacon[2]
    R.append((x,y,z))
  
  XA = [(1, 0, -1, 0), (0, 0, 0, 0), (0, -1, 0, 1)]
  YA = [(0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 0, 0)]
  ZA = [(0, 1, 0, -1), (0, 0, 0, 0), (1, 0, -1, 0)]
  R2 = []
  for r in R:
    for ya in range(4):
      x = XA[0][ya] * r[0] + XA[1][ya] * r[1] + XA[2][ya] * r[2]
      y = YA[0][ya] * r[0] + YA[1][ya] * r[1] + YA[2][ya] * r[2]
      z = ZA[0][ya] * r[0] + ZA[1][ya] * r[1] + ZA[2][ya] * r[2]
      if (x,y,z) not in R2:
        R2.append((x,y,z))

  XA = [(1, 0, -1, 0), (0, -1, 0, 1), (0, 0, 0, 0)]
  YA = [(0, 1, 0, -1), (1, 0, -1, 0), (0, 0, 0, 0)]
  ZA = [(0, 0, 0, 0), (0, 0, 0, 0), (1, 1, 1, 1)]
  R3 = []
  for r in R2:
    for za in range(4):
      x = XA[0][za] * r[0] + XA[1][za] * r[1] + XA[2][za] * r[2]
      y = YA[0][za] * r[0] + YA[1][za] * r[1] + YA[2][za] * r[2]
      z = ZA[0][za] * r[0] + ZA[1][za] * r[1] + ZA[2][za] * r[2]
      if (x,y,z) not in R3:
        R3.append((x,y,z))
        
  return R3

for line in lines:
  if "---" in line:
    print(line)
    nextScanner = []
  else:
    if line == "":
      S.append(nextScanner)
    else:
      x,y,z = [int(x) for x in line.split(",")]
      nextScanner.append((x,y,z))
S.append(nextScanner)

B = S[0]

def findPos(BOARD, bacons):
  B = []
  for b in bacons:
    rots = rotations(b)
    B.append(rots)
  
  maxMatch = -10e9
  maxMatchi = None
  offxfinal = None
  offyfinal = None
  offzfinal = None

  for i in range(24):
    for baconinboard in BOARD:
      for bi in range(len(B)):
        #print("Maxing", baconinboard, "with", B[bi][i])
        offx = baconinboard[0] - B[bi][i][0]
        offy = baconinboard[1] - B[bi][i][1]
        offz = baconinboard[2] - B[bi][i][2]
        
        TOMATCH = []
        for bi2 in range(len(B)):
          TOMATCH.append(B[bi2][i])
        
        match = 0
        for baconinboard2 in BOARD:
          x = baconinboard2[0] - offx
          y = baconinboard2[1] - offy
          z = baconinboard2[2] - offz
          
          if (x,y,z) in TOMATCH:
            match += 1

        assert(match >= 1)
        
        if match > maxMatch:
          maxMatch = match
          maxMatchi = i
          offxfinal = offx
          offyfinal = offy
          offzfinal = offz
          
    
  print("Max Match", maxMatch)
  assert(maxMatch >= 12)
  print("Matched", maxMatch)
  MACHED = []
  for bi2 in range(len(B)):
    x = B[bi2][maxMatchi][0] + offxfinal
    y = B[bi2][maxMatchi][1] + offyfinal
    z = B[bi2][maxMatchi][2] + offzfinal
    MACHED.append((x,y,z))

  print("Relative", offxfinal, offyfinal, offzfinal)
  return MACHED

rots = rotations((1,2,3))
tocheck = [(1,2,3),
           (1,-2,-3),
           (1,3,-2),
           (1,-3,2),
           
           (1,2,3),
           (-1,2,-3),
           (-3,2,1),
           (3,2,-1),
           
           (1,2,3),
           (-1,-2, 3),
           (2,-1, 3),
           (-2,1, 3)
           
           ]
for check in tocheck:
  if check not in rots:
    print("not in", check)
    assert(0)

print(B)
print("Len", len(B))
for i in range(1, len(S)):
  newPos = findPos(S[0], S[i])
  npcount = 0
  for np in newPos:
    if np not in B:
      B.append(np)
    else:
      print("Already matched", np)
      npcount += 1
  print("Count", npcount, len(newPos)-npcount)
  print("Len", len(B))

print("Part1", len(B))
