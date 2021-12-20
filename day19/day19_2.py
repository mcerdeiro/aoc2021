#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq
from multiprocessing import Pool

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day19.dat", "r").read().splitlines()

lines2= open("res.dat", "r").read().splitlines()
RES = []
for l in lines2:
  RES.append(tuple(int(x) for x  in l.split(",")))


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
   
def getRotations(bacon):
  ret = []

  for roll in range(2):
      for yaw in range(4):
        for pitch in range(4):
          ret.append(rotationangle(bacon, pitch, roll, yaw))

  return ret

def scannersWithRotations(S):
  ret = []
  
  for s in S:
    tmp = []
    for b in s:
      tmp.append(getRotations(b))
    ret.append(tmp)
  
  return ret

def parseScanners(lines):
  S = []
  tmp = []
  for line in lines:
    if "---" in line:
      print(line)
    elif line == "":
      S.append(tmp)
      print("Len", len(tmp))
      tmp = []
    else:
      x,y,z = [int(x) for x in line.split(",")]
      tmp.append((x,y,z))
  
  if len(tmp) != 0:
    S.append(tmp)
    print("Len", len(tmp))
  
  return S

def move(overlap, ri, ref):
  ret = []
  for p in overlap:
    assert(len(p)==32)
    assert(len(ref)==3)
    x = p[ri][0]-ref[0]
    y = p[ri][1]-ref[1]
    z = p[ri][2]-ref[2]
    ret.append((x,y,z))
  return ret


def getRotPoints(points, rotindex):
  ret = []
  for p in points:
    ret.append(p[rotindex])
  return ret

def translate(points, translation):
  ret = []
  for p in points:
    x = p[0] - translation[0]
    y = p[1] - translation[1]
    z = p[2] - translation[2]
    ret.append((x,y,z))
  return ret

def foundOverlap(ref, overlap):
  assert(len(overlap[0])==32)
  for rotindex in range(len(overlap[0])):
    rotpoints = getRotPoints(overlap, rotindex)
    for r1 in ref:
      for r2 in rotpoints:
        offx = r2[0] - r1[0]
        offy = r2[1] - r1[1]
        offz = r2[2] - r1[2]
        trans = translate(rotpoints, (offx, offy, offz))
        match = 0
        for t in trans:
          if t in ref:
            match += 1
        if match >= 12:
          return trans, (-offx, -offy, -offz)
    
  return None, None

S = parseScanners(lines)
S = scannersWithRotations(S)


FOUNDS = [0]
NOTFOUNDS = [x for x in range(1, len(S))]
BOARD = getRotPoints(S[0], 0)
TRANSFORMED = {0: getRotPoints(S[0], 0)}
SPOS = [(0,0,0)]

print("Found", FOUNDS, "notfound", NOTFOUNDS)
I = set()

def checkParallel(input):
  global TRANSFORMED, S, I
  f = input[0]
  nf = input[1]
  if (f,nf) in I:
        return None, None

  print("Checking", f, nf)
  assert(f in TRANSFORMED.keys())
  transformed, scanpos = foundOverlap(TRANSFORMED[f], S[nf])
  return transformed, scanpos

while len(NOTFOUNDS) != 0:
  print("Still not found", NOTFOUNDS, I)
  
  PINPUT = []
  for f in FOUNDS:
    PINPUT = [(f, nf) for nf in NOTFOUNDS]
    ret = []
    with Pool(8) as pools:
      res = pools.map(checkParallel, PINPUT)
    #for nf in NOTFOUNDS:
      # if (f,nf) in I:
      #   continue
      # print("Checking", f, nf)
      # transformed, scanpos = foundOverlap(TRANSFORMED[f], S[nf])
    for i,r in enumerate(res):
      transformed, scanpos = r
      f = PINPUT[i][0]
      nf = PINPUT[i][1]
      if transformed == None:
        I.add((f,nf))
        pass
      else:
        SPOS.append(scanpos)
        FOUNDS.insert(0, nf)
        NOTFOUNDS.remove(nf)
        oldlen = len(BOARD)
        for t in transformed:
          if t not in BOARD:
            BOARD.append(t)
        TRANSFORMED[nf] = transformed.copy()
        print("Oldlen", oldlen, "newlen", len(BOARD), len(transformed))
    
print("Part1:", len(BOARD))
print(SPOS)


def manDistance(p1, p2):
  return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]) + abs(p1[2]-p2[2])

maxD = 0
for i in range(len(SPOS)):
  for j in range(len(SPOS)):
    if i != j:
      maxD = max(maxD, manDistance(SPOS[i], SPOS[j]))
      
print("Part2", maxD)