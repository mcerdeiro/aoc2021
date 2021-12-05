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
      
D = dict()

def drawLine(x0,y0,x1,y1):
  if (x0 == x1):
    for i in range(min(y0, y1), max(y0, y1)+1):
      if (x0, i) in D.keys():
        D[(x0,i)] += 1
      else:
        D[(x0,i)] = 1
  elif (y0 == y1):
    for i in range(min(x0, x1), max(x0,x1)+1):
      if (i, y0) in D.keys():
        D[(i,y0)] += 1
      else:
        D[(i,y0)] = 1
  else:
    xs = min(x0,x1)
    xe = max(x0,x1)+1
    ys = y0
    if xs == x1:
      ys = y1
    
    ye = y0
    if ys == y0:
      ye = y1
    
    p = 1
    if ye < ys:
      p = -1
      
    for x in range(xs,xe):
      y = ys + p * (x-xs)
      if (x,y) in D.keys():
        D[(x,y)] += 1
      else:
        D[(x,y)] = 1
    
        

def printBoard():
  for i in range(10):
    tmp = ""
    for j in range(10):
      if (j,i) in D.keys():
        #print(D[(j,i)])
        tmp += str(D[(j,i)])
      else:
        tmp += "."
        
    print(tmp)

def part1and2(inputfile):
  lines = open(inputfile, "r").read().splitlines()
  for line in lines:
    ps, pe = line.split(" -> ")
    x0, y0 = [int(x) for x in ps.split(",")]
    x1, y1 = [int(x) for x in pe.split(",")]
    if (x0 == x1) or (y0 == y1):
      drawLine(x0,y0,x1,y1)
  
  p1 = 0
  for k in D.keys():
    if D[k] > 1:
      p1 += 1
    
  print("Part1", p1)
  
  for line in lines:
    ps, pe = line.split(" -> ")
    x0, y0 = [int(x) for x in ps.split(",")]
    x1, y1 = [int(x) for x in pe.split(",")]
    if (x0 != x1) and (y0 != y1):
      drawLine(x0,y0,x1,y1)

  p2 = 0
  for k in D.keys():
    if D[k] > 1:
      p2 += 1
    
  print("Part2", p2)

#assert_print(lambda :part1and2("ex01.dat"))
assert_print(lambda :part1and2("day05.dat"))
