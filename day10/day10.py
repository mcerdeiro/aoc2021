#!/usr/bin/python3
import copy
from typing import List
import sys

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day10.dat", "r").read().splitlines()
convert = { "<": ">", "(": ")", "[": "]", "{": "}"}

def findFirstIlegalCharacter(line):
  LIST = []  
  for c in line:
    if c in ["<", "[", "{", "("]:
      LIST.append(c)
    elif c in [">", "]", "}", ")"]:
      l = LIST.pop()
      if convert[l] != c:
        return c, LIST
    else:
      assert(0)
      
  return "", LIST

P1 = {
  ")": 3,
  "]": 57,
  "}": 1197,
  ">": 25137
}

P2 = {
  ")": 1,
  "]": 2,
  "}": 3,
  ">": 4
}
 
p1 = 0
p2 = 0
VALS = set()

for line in lines:
  i, L = findFirstIlegalCharacter(line)
  if i != "":
    p1 += P1[i]
  else:
    score = 0
    for l in L[::-1]:
      score *= 5
      score += P2[convert[l]]
  
  VALS.add(score)

print("Part 1:", p1)

VALS = list(VALS)
VALS.sort()

print("Part 2:", VALS[len(VALS)//2])