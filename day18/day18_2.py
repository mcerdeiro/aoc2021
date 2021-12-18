#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day18.dat", "r").read().splitlines()

def explode(L, i):
  print("explode", L[i:i+5])
  v1 = int(L[i])
  v2 = int(L[i+2])
  print(v1, v2)
  for i1 in range(i+3, len(L)):
    if L[i1].isnumeric():
      newVal = int(L[i1]) + v2
      #print("newval", newVal, i1)
      L = L[0:i1] + str(newVal) + L[i1+1:]
      break
  for i1 in range(i-1,0,-1):
    if L[i1].isnumeric():
      newVal = int(L[i1]) + v1
      L = L[0:i1-1] + str(newVal) + L[i1+1:]
      break
  
  L = L[0:i-1] + str(0) + L[i+4:]
  
  return L


def reduce(L):
  level = 0
  for i,v in enumerate(L):
    if level == 4:
      print("To explode", L, i)
      L = explode(L, i+1)
      print("Af explode", "\"" + L + "\"")
      return L
    if v in ["["]:
      level += 1
    if v in ["]"]:
      level -= 1
    
  
  return L
      
    
assert(reduce("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]")
reduce("[7,[6,[5,[4,[3,2]]]]]")
exit()

for line in lines:
  line = reduce(line)