#!/usr/bin/python3

import copy
from typing import List

def assert_print(func, expected = None):
  val = func()
  if expected == None:
    print("Result:", val)
  else:
    if val == expected:
      print("OK", val)
    else:
      print("FAILED expected", expected, "returned", val)

def part1and2(inputfile):
  lines = open(inputfile, "r").read().splitlines()
  N = [int(x) for x in lines[0].split(",")]
  G = [N.count(x) for x in range(9)]

  for i in range(80):
    G = G[1:] + G[:1]
    G[6] += G[-1]

  print("Part1:", sum(G))

  for i in range(256-80):
    G = G[1:] + G[:1]
    G[6] += G[-1]

  print("Part2:", sum(G))

#assert_print(lambda :part1and2("ex01.dat"))
assert_print(lambda :part1and2("day06.dat"))
