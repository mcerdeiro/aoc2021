#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day20.dat", "r").read().splitlines()

ans1 = 0 

FIRST = None
M = {}
OTHERS = "0"

y = 0
for line in lines:
  if FIRST == None:
    FIRST = line
  else:
    if line != "":
      for x in range(len(line)):
        M[(x,y)] = line[x]
      y += 1
    
def getVal(p):
  global OTHERS
  if p in M.keys():
    if M[p] == "#":
      return "1"
    return "0"
  else:
    return OTHERS
  

def getNeisValue(p):
  tmp = ""
  for y in [-1,0,1]:
    for x in [-1,0,1]:
      tmp += getVal((p[0]+x, p[1]+y))

  return int(tmp,2)

      

def getValues(p):
  global FIRST
  neis = getNeisValue(p)
  return FIRST[neis]
  
  
def update(M):
  global OTHERS
  M2 = {}
  
  for x in range(-100, 200):
    for y in range(-100, 200):
      M2[(x,y)] = getValues((x,y))
      
  OTHERS = [OTHERS for x in range(9)]
  OTHERS = FIRST[int(''.join(OTHERS),2)]
  if OTHERS == "#":
    OTHERS = "1"
  else:
    OTHERS = "0"
  return M2

def printGraph(M):
  for y in range(-20,120):
    tmp = ""
    for x in range(-20, 120):
      if (x,y) in M.keys():
        tmp += M[(x,y)]
      else:
        tmp += OTHERS
    print(tmp)
    

def getOn():
  ret = 0
  for v in M.keys():
    if M[v] == "#":
      ret += 1

  return ret

for i in range(50):
  if i == 2:
    print("Part1:", getOn())
  M = update(M)
print("Part2", getOn())




