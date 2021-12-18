#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day18.dat", "r").read().splitlines()

ans = 0

def processLine(line):
  val = []
  offset = -1
  for i, v in enumerate(line):
    if offset < 0:
      tmp = []
      if v in ["[", "]", ","]:
        if v in ["["]:
          offset, V = processLine(line[i+1:])
          val.append(V)
        if v in ["]"]:
          #print("Return", i, val)
          return i+1, val
      else:
        val.append(int(v))
    else:
      offset -= 1
      if offset == 0:
        offset = -1
      
  return i, val

def exploide(vals, level = 0):
  v1 = -1
  v2 = -1
  for i, v in enumerate(vals):
    if level == 4:
      print("Exploding", v[0])
      v1 = v[0][0]
      v2 = v[0][1]
      
      if type(v[1]) == int:
        v[1] += v2
        v2 = -1
      v[0] = 0
      return "EXP", v1, v2
    if type(v) == list:
      e, v1, v2 = exploide(v, level+1)
      return "DONE", v1, v2

  return "DONE", v1, v2


def reduce(line):
  V = processLine(line)
  exploide(V)
  print(V)
  
  return 0

L = processLine("[[[[[9,8],1],2],3],4]")
print(L)

# reduce()
# [[[[0,9],2],3],4]
exit()

for line in lines:
  ans += reduce(line)
  
print("Part1: ", ans)