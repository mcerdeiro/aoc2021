#!/usr/bin/python3

def countDepthMessurementIncreases(values):
  count = 0
  last = None
  for value in values:
    if last != None and value > last:
      count += 1
    last = value
  return count

def groupValsInGroupsOf3(values):
  group = []
  for i in range(len(values)-2):
    group.append(values[i]+values[i+1]+values[i+2])
    
  return group


lines = open("day01.dat", "r").read().splitlines()
vals = [int(x) for x in lines]

print("Part1:", countDepthMessurementIncreases(vals))
print("Part2:", countDepthMessurementIncreases(groupValsInGroupsOf3(vals)))
  
  

