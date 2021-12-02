#!/usr/bin/python3

lines = open("day02.dat", "r").read().splitlines()

def mulHorizontalAndDepthPosition(movements):
  pos = (0, 0) # forward, depth
  moveTypes = {"forward": (1,0), "down": (0, 1), "up": (0, -1)}
  for move in movements:
    dir, moves =  move.split(" ")
    moves = int(moves)
    pos = (pos[0] + moveTypes[dir][0] * moves, 
           pos[1] + moveTypes[dir][1] * moves)

  # return forward * depth
  return pos[0] * pos[1]
    
def mulHorizontalAndDepthPositionWithAim(movements):
  pos = (0, 0, 0) # forward, aim, depth
  moveTypes = {"forward": (1,0, 1), "down": (0, 1, 0), "up": (0, -1, 0)}
  for move in movements:
    dir, moves =  move.split(" ")
    moves = int(moves)
    pos = (pos[0] + moveTypes[dir][0] * moves, 
           pos[1] + moveTypes[dir][1] * moves,
           pos[2] + moveTypes[dir][2] * pos[1] * moves)

  # return forward * depth
  return pos[0] * pos[2]

print("Part1: ", mulHorizontalAndDepthPosition(lines))
print("Part2: ", mulHorizontalAndDepthPositionWithAim(lines))
  

