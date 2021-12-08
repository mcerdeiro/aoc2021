#!/usr/bin/python3
import copy
from typing import List

lines = open("day07.dat", "r").read().splitlines()

vals = [int(x) for x in lines[0].split(",")]

def fuelCostPart2(val):
  return int (val * (val + 1) * 0.5)

def fuelCostPart1(val):
  return val


mini = min(vals)
maxi = max(vals)

minFuelPart1 = 10e9
minFuelPart2 = 10e9

for check in range(mini,maxi):
  fuelPart1 = 0
  fuelPart2 = 0
  for val in vals:
    fuelPart1 += fuelCostPart1(abs(check - val))
    fuelPart2 += fuelCostPart2(abs(check - val))

  minFuelPart1 = min(minFuelPart1, fuelPart1)
  minFuelPart2 = min(minFuelPart2, fuelPart2)

print("Part1:", minFuelPart1)
print("Part2:", minFuelPart2)
