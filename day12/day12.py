#!/usr/bin/python3
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day12.dat", "r").read().splitlines()

C = {}
for line in lines:
  fr,to = line.split("-")
  if to != "start":
    if fr in C.keys():
      C[fr] += [to]
    else:
      C[fr] = [to]
  if fr != "start":
    if to in C.keys():
      C[to] += [fr]
    else:
      C[to] = [fr]

for k,vals in C.items():
  if k.islower():
    newvals = []
    for v in vals:
      if v.islower():
        newvals.append(v)
      else:
        for v2 in C[v]:
          newvals.append(v2)
        
    C[k] = newvals
        


def isValidCombinationPart1(path, current):
  if current.isupper():
    return True
  if path.count(current) == 0:
    return True
  
  return False
  
  
def isValidCombinationPart2(path, current, smallCaveTwice = False):
  if current.islower():    
    if current == "start":
      return False

    countCurrent = path.count(current)
    if smallCaveTwice:
      if countCurrent >= 1:
        return False
    else:
      if countCurrent >= 2:
        return False  
  return True
  
p1 = 0
p2 = 0

def findPathsPart1(current):
  global p1

  if current[-1] == "end":
    p1 += 1
    return

  options = C[current[-1]]
  for opt in options:
    if isValidCombinationPart1(current, opt):
      new = copy.deepcopy(current)
      new.append(opt)
      findPathsPart1(new)

def findPathsPart2(current, smallCaveTwice = False):
  global p1, p2

  if current[-1] == "end":
    p2 += 1
    return

  options = C[current[-1]]
  for opt in options:
    if (isValidCombinationPart2(current, opt, smallCaveTwice)):
      followSmallCaveTwice = smallCaveTwice
      if followSmallCaveTwice == False:
        if opt.islower():
          if current.count(opt) == 1:
            followSmallCaveTwice = True
      new = copy.deepcopy(current)
      new.append(opt)
      findPathsPart2(new, followSmallCaveTwice)


findPathsPart1(["start"])
print("Part1:", p1)
# findPathsPart2(["start"])
# print("Part2:", p2)

p2 = 0
def findPathsPart2_2(path: set(), last: str,  alreadyInSmallCaveTwice: bool = False):
  global p2
  
  options = C[last]
  for opt in options:
    if opt.isupper():
      findPathsPart2_2(path, opt, alreadyInSmallCaveTwice)
    else:
      if opt == "end":
        p2 += 1
      else:
        if opt in path:
          if not alreadyInSmallCaveTwice:
            findPathsPart2_2(path, opt, True)
        else:
          newpath = set(path)
          newpath.add(opt)
          findPathsPart2_2(newpath, opt, alreadyInSmallCaveTwice)
  

findPathsPart2_2(set(), "start", False)
print("Optimized Part2:", p2)