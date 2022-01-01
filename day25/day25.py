#!/usr/bin/python3
import sys
import heapq
import copy

debug = True

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day25.dat", "r").read().splitlines()

M = {}
X = 0
Y = 0

for y in range(len(lines)):
  for x in range(len(lines[y])):
    M[(x,y)] = lines[y][x]
    X = max(x+1, X)
    Y = max(y+1, Y)



def moveEastAndSouth(M):
  moves = 0
  tomoveEast = []
  for y in range(Y):
    for x in range(X):
      if M[(x,y)] == ">":
        pos = (x+1, y)
        if pos not in M:
          pos = (0, y)
        if M[pos] == ".":
          tomoveEast.append([(x,y), pos])

  moves += len(tomoveEast)          
  for tome in tomoveEast:
    fr,to = tome
    M[fr] = "."
    M[to] = ">"


    
  tomoveSouth = []
  for y in range(Y):
    for x in range(X):
      if M[(x,y)] == "v":
        pos = (x, y+1)
        if pos not in M:
          pos = (x, 0)
        if M[pos] == ".":
          tomoveSouth.append([(x,y), pos])
          
  moves += len(tomoveSouth)
  for tome in tomoveSouth:
    fr,to = tome
    M[fr] = "."
    M[to] = "v"
          
  return moves

def printMap(M):
  for y in range(Y):
    tmp = ""
    for x in range(X):
      tmp += M[(x,y)]
    print(tmp)

ans1 = 1
moves = moveEastAndSouth(M)
while moves > 0:
  moves = moveEastAndSouth(M)
  ans1 += 1  
  
print("Part1:", ans1)
  
  