#!/usr/bin/python3
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day12.dat", "r").read().splitlines()

C = {}
for line in lines:
  fr,to = line.split("-")
  if fr in C.keys():
    C[fr] += [to]
  else:
    C[fr] = [to]
  if to in C.keys():
    C[to] += [fr]
  else:
    C[to] = [fr]
    
def getLows(path):
  lows = defaultdict(int)
  for p in path:
    if p.islower():
      lows[p] += 1
  return lows

def isValidCombinationPart1(path):
  lows = getLows(path)
  if list(lows.values()).count(2) > 0:
    return False
  return True
  
  
def isValidCombinationPart2(path):
  lows = getLows(path)

  if list(lows.values()).count(3) == 1:
    return False
  if list(lows.values()).count(2) == 2:
    return False
  if lows["start"] > 1:
    return False
  
  return True
  
p1 = 0
p2 = 0

def findPathsPart(current):
  global p1, p2

  if current[-1] == "end":
    if isValidCombinationPart1(current):
      p1 += 1
    p2 += 1
    return

  options = C[current[-1]]
  for opt in options:
    new = copy.deepcopy(current)
    new.append(opt)
    if (isValidCombinationPart2(new)):
      findPathsPart(new)


findPathsPart(["start"])
print("Part1:", p1)
print("Part2:", p2)
