#!/usr/bin/python3
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day14.dat", "r").read().splitlines()

S = None
INSERT = {}
TEMP = None

def count(TEMP):
  POLY = defaultdict(int)
  for k,v in TEMP.items():
    POLY[k[0]] += v
  return POLY

for line in lines:
  if line != "":
    if TEMP == None:
      TEMP = defaultdict(int)
      line += " "
      for i in range (len(line)-1):
        TEMP[line[i:i+2]] += 1
    else:
      fr,to = line.split(" -> ")
      INSERT[fr] = to

for i in range(40):
  TEMP2 = defaultdict(int)
  for k in TEMP.keys():
    if TEMP[k] > 0:
      if k in INSERT.keys():
        TEMP2[k[0] + INSERT[k]] += TEMP[k]
        TEMP2[INSERT[k] + k[1]] += TEMP[k]
      else:
        TEMP2[k] = TEMP[k]

  TEMP = TEMP2
    
  if i == 9:
    POLY = count(TEMP)
    print("Part1:", max(POLY.values()) - min(POLY.values()))

POLY = count(TEMP)
print("Part2:", max(POLY.values()) - min(POLY.values()))
