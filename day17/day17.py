#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day17.dat", "r").read().splitlines()

def move(x,y, vx, vy):
  x = x + vx
  y = y + vy
  
  if vx > 0:
    vx -= 1
  if vx < 0:
    vx += 1
  
  vy -= 1
  
  return x,y,vx,vy

x = 0
y = 0
vx = 7
vy = 2

TX = []
TY = []

for line in lines:
  x1,x2 = line.split("target area: x=")[1].split(", y=")[0].split("..")
  TX.append(int(x1))
  TX.append(int(x2))
  y1,y2 = line.split("target area: x=")[1].split(", y=")[1].split("..")
  TY.append(int(y1))
  TY.append(int(y2))
  
def check(vx, vy, TX, TY):
  Y = -10e9
  x = 0
  y = 0
  while True:
    #print(i, ":", x,y)
    x,y,vx,vy = move(x,y,vx,vy)
    Y = max(Y, y)
    if TX[0] <= x <= TX[1] and TY[0] <= y <= TY[1]:
      return True, Y
    if y < TY[0]:
      return False, Y
    if vx == 0 and not (TX[0] <= x <= TX[1]):
      return False, Y
    if x > TX[1] and vx >= 0:
      return False, Y
    if x < TX[0] and vx <= 0:
      return False, Y
    
  return False, Y

# x = 0
# y = 0
# vx = 11
# vy = 170
# for i in range(100):
#   x,y,vx,vy = move(x,y,vx,vy)
#   print("aca", x,y,vx,vy)
#   if TX[0] <= x <= TX[1] and TY[0] <= y <= TY[1]:
#       print("YDD")
#       exit()
  
# exit()

Y = -10e9
p2 = 0

for vx in range(500):
  #print("", vx, Y)
  for vy in range(-1000,500):
    r,y = check(vx,vy,TX,TY)
    if (r == True):
      p2 += 1
      Y = max(Y, y)
    
    
  
print("Part 1", Y)
print("Part 2", p2)