#!/usr/bin/python3
import itertools
from functools import reduce 

def countDepthMessurementIncreases(values):
  ret = 0
  old = None
  for v in values:
    if old != None and v > old:
      ret += 1
    old = v
  return ret

def groupValsInGroupsOf3(values):
  grouped = []
  for i in range(len(values)-2):
    grouped.append(values[i]+values[i+1]+values[i+2])
    
  return grouped


lines = open("day01.dat", "r").read().splitlines()
vals = [int(x) for x in lines]

print("Part2:", countDepthMessurementIncreases(vals))
print("Part2:", countDepthMessurementIncreases(groupValsInGroupsOf3(vals)))
  
  

