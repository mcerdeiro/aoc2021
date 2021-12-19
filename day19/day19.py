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

def getrotations(bacon):
  ret = []
  for ax in [1, -1]:
    for ay in [1, -1]:
      for az in [1, -1]:
        x = bacon[0] * ax
        y = bacon[1] * ay
        z = bacon[2] * az
        
        ret.append((x,y,z))
    
  ret2 = []
  for r in ret:
    for rot in [0, 1,2]:
      x,y,z = r
      if rot == 0:
        ret2.append((x,y,z))
      elif rot == 1:
        ret2.append((y,z, x))
      elif rot == 2:
        ret2.append((z, x, y))

  assert(len(set(ret2))==24)
  return ret2

#R = getrotations((1,2,3))
#print(len(R), len(set(R)), R)

        
        

def rotationangle(bacon, pitch, roll, yaw):
  cosa = [1, 0, -1, 0][yaw] # cos 0, 90, 180, 270 = 1, 0, -1, 0
  sina = [0, 1, 0, -1][yaw] # cos 0, 90, 180, 270 = 0, 1, 0, -1
  
  cosb = [1, 0, -1, 0][pitch] # cos 0, 90, 180, 270 = 1, 0, -1, 0
  sinb = [0, 1, 0, -1][pitch] # cos 0, 90, 180, 270 = 0, 1, 0, -1
  
  cosc = [1, 0, -1, 0][roll] # cos 0, 90, 180, 270 = 1, 0, -1, 0
  sinc = [0, 1, 0, -1][roll] # cos 0, 90, 180, 270 = 0, 1, 0, -1
  
  Axx = cosa*cosb
  Axy = cosa*sinb*sinc - sina*cosc
  Axz = cosa*sinb*cosc + sina*sinc

  Ayx = sina*cosb
  Ayy = sina*sinb*sinc + cosa*cosc
  Ayz = sina*sinb*cosc - cosa*sinc

  Azx = -sinb
  Azy = cosb*sinc
  Azz = cosb*cosc
  
  px,py,pz = bacon
  x = Axx*px + Axy*py + Axz*pz
  y = Ayx*px + Ayy*py + Ayz*pz
  z = Azx*px + Azy*py + Azz*pz
  
  return (x,y,z)
  
def getAllRotations(bacon):
  ret = []
  for pitch in range(4):
    for roll in range(4):
      for yaw in range(4):
        ret.append(rotationangle(bacon, pitch, roll, yaw))

  return ret

def rotationsNotUSe(bacon):
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
      #if (x,y,z) not in R2:
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
      #if (x,y,z) not in R3:
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

def findPos(BOARD, bacons):
  B = []
  for b in bacons:
    rots = getrotations(b)
    B.append(rots)
  
  maxMatch = -10e9
  maxMatchi = None
  offxfinal = None
  offyfinal = None
  offzfinal = None

  for i in range(len(B[0])):
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

  #assert(maxMatch >= 12)
  print("Matching", maxMatch)
  if maxMatch < 12:
    return None
  
  TRANSFORMED = []
  for bi2 in range(len(B)):
    x = B[bi2][maxMatchi][0] + offxfinal
    y = B[bi2][maxMatchi][1] + offyfinal
    z = B[bi2][maxMatchi][2] + offzfinal
    TRANSFORMED.append((x,y,z))

  #print("Relative", maxMatchi, offxfinal, offyfinal, offzfinal)
  return TRANSFORMED

B = S[0]

TRULE = {}
MATCHED = [0]

while(len(MATCHED) != 4):
  for i in range(len(S)):
    for j in range(len(S)):
      if j != i:
        print("Checking", i, j)
        if i in MATCHED and j not in MATCHED:
          TRANS = findPos(S[i], S[j])
          if TRANS != None:
            S[j] = TRANS
            MATCHED.append(j)
            for t in TRANS:
              if t not in B:
                B.append(t)
            print("Sensor", i, "matches", j, MATCHED)


print(MATCHED)
print("Part1", len(B))  

# while (len(MATCHED) != 5):
#   for i in range(len(S)):
#     for j in range(i+1, len(S)):
#       print("Checking", i, j)
#       if i != j:
#         newPos, matchi, offx, offy, offz = findPos(S[i], S[j])
#         if newPos != None:
#           if i in MATCHED:
#             if j not in MATCHED:
#               print("Sensor", i, "matches", j)
#               #print("S[j]", S[j])
#               #print("newPos", newPos)
#               S[j] = newPos
#               MATCHED.append(j)
#               for np in newPos:
#                 if np not in B:
#                   B.append(np)

# print(MATCHED)
# print("Part1", len(B))
