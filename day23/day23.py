#!/usr/bin/python3
import sys
import heapq
import copy

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day23.dat", "r").read().splitlines()
part2 = False

def printMap(M, M2 = None):
  cost = M["score"]
  for y in range(7):
    tmp = ""
    for x in range(90):
      if (x,y) in M:
        tmp += M[(x,y)][0]
      elif x < 20:
        tmp += " "
      if 40 >= x >= 20:
        if M2 != None:
          if (x-20,y) in M2:
            tmp += M2[(x-20,y)][0]
          else:
            tmp += " "
      if x >= 40:
        if M2 != None:
          if (x-40,y) in M2:
            if M2[(x-40,y)][0] in ["A", "B", "C", "D"]:
              tmp += str(M2[(x-40,y)][1])
            else:
              tmp += " "
    if cost != None:
      tmp += "    Cost: " + str(cost)
      cost = None
    print(tmp)

def getGoalColumn(amphipods):
  if amphipods == "A":
    return 3
  elif amphipods == "B":
    return 5
  elif amphipods == "C":
    return 7
  elif amphipods == "D":
    return 9
  else:
    assert(0)
    
def calculateCost(let, length):
  mul = 1
  if let == "A":
    mul = 1
  elif let == "B":
    mul = 10
  elif let == "C":
    mul = 100
  elif let == "D":
    mul = 1000
  else:
    assert(0)
    
  if mul*length == 0:
    assert(mul*length != 0)
  return mul * length

def inGoal(pos, MAP):
  goalCol = getGoalColumn(MAP[pos][0])
  if pos[0] != goalCol:
    return False
  lastPos = 3
  if part2:
    lastPos = 5
  for i in range(lastPos,1, -1):
    if MAP[(goalCol,i)][0] != MAP[pos][0]:
      return False
    if i == pos[1]:
      return True
  
  return True

def getGoal(amphipods, MAP):
  col = getGoalColumn(amphipods)
  lastRow = 3
  if part2:
    lastRow = 5

  while MAP[(col, lastRow)][0] == amphipods:
    lastRow -= 1

  if lastRow > 1:
    if MAP[(col, lastRow)][0] == ".":
      return (col, lastRow)

  return None
  
def performMove(fr, to, cost, MAP):
  assert(MAP[fr][1] < 2)
  if to[1] > 1:
    MAP[to] = (MAP[fr][0], 2)
  else:
    MAP[to] = (MAP[fr][0], MAP[fr][1]+1)
  MAP[fr] = (".", 0)
  MAP["score"] += cost
  
  
def moveLenght(fr, to, MAP):
  movedirs = []
  currentpos = fr
  movements = 0
  if fr[1] != 1:
    movedirs.append("up")
  movedirs.append("lateral")
  if to[1] != 1:
    movedirs.append("down")
  debug = False
  for move in movedirs:
    if move == "up":
      dir = -1
      currentpos = (currentpos[0], currentpos[1]+dir)
      movements += 1
      while currentpos[1] != 1:
        movements += 1
        if MAP[currentpos][0] != ".":
          return None
        currentpos = (currentpos[0], currentpos[1]+dir)
      if MAP[currentpos][0] != ".":
          return None
    if move == "lateral":
      dir = (to[0]-fr[0])//abs(to[0]-fr[0])
      currentpos = (currentpos[0]+dir, currentpos[1])
      movements += 1
      while currentpos[0] != to[0]:
        movements += 1
        if MAP[currentpos][0] != ".":
          return None
        currentpos = (currentpos[0]+dir, currentpos[1])
      if MAP[currentpos][0] != ".":
          return None
    if move == "down":
      dir = 1
      currentpos = (currentpos[0], currentpos[1]+dir)
      movements += 1
      while currentpos[1] != to[1]:
        movements += 1
        if MAP[currentpos][0] != ".":
          return None
        currentpos = (currentpos[0], currentpos[1]+dir)
      if MAP[currentpos][0] != ".":
          return None
  
  assert(currentpos == to)
  assert(movements != 0)
  return movements

def getLetters(MAP):
  letters = []
  for m in MAP:
    if m == "score":
      continue
    if MAP[m][0] in ["A", "B", "C", "D"]:
      letters.append(m)
      
  return letters

def getPossibleLettersToMove(MAP):
  letters = getLetters(MAP)
  lettersThatCanBeMoved = []
  for let in letters:
    # if letter allready moved twice can not be moved again
    if MAP[let][1] == 2:
      assert(inGoal(let, MAP) == True)
      continue
    if let[1] != 1:
      if MAP[(let[0], let[1]-1)][0] != ".":
        continue
    if MAP[(let[0]-1, 1)][0] != "." and MAP[(let[0]+1, 1)][0] != ".":
      continue
    lettersThatCanBeMoved.append(let)
    
  return lettersThatCanBeMoved

def getPossibleMovesWithPriosFor(fr, MAP):
  moves = []
  goal = getGoal(MAP[fr][0], MAP)
  if goal != None:
    movements = moveLenght(fr, goal, MAP)
    if movements != None:
      moves.append((-100, fr, goal, calculateCost(MAP[fr][0], movements)))
      return moves
  if fr[1] != 1:
    for i in range(1,12):
      if i in [3,5,7,9]:
        continue
      to = (i, 1)
      movements = moveLenght(fr, to, MAP)
      if movements != None:
        # check if the new position is a middle position to the goal or a detour
        goalCol = getGoalColumn(MAP[fr][0])
        detour = True
        if fr[0] < to[0] < goalCol:
          detour = False
        moves.append((-10 if not detour else 0, fr, to, calculateCost(MAP[fr][0], movements)))
  return moves

def getPossibleMovesByPrio(MAP):
  moves = []
  lettersThatCanBeMoved = getPossibleLettersToMove(MAP)
  for let in lettersThatCanBeMoved:
    moves += getPossibleMovesWithPriosFor(let, MAP)
  moves = sorted(moves, key=lambda x: x[0])
  return moves

def allAtFinishPosition(MAP):
  letters = getLetters(MAP)
  for let in letters:
    if not inGoal(let, MAP):
      return False
    
  return True

DP = {}
currentMin = 10e9
def solve(MAP: dict):
  global currentMin
  
  score = MAP.pop("score")
  if tuple(MAP.items()) in DP:
    return DP[tuple(MAP.items())]
  MAP["score"] = score

  if allAtFinishPosition(MAP):
    return 0

  minCost = 10e9
  moves = getPossibleMovesByPrio(MAP)
  for move in moves:
    if MAP["score"]+move[3] < currentMin:
      newMap = MAP.copy()
      performMove(move[1], move[2], move[3], newMap)
      tmp = solve(newMap)
      tmp += move[3]
      if tmp < minCost:
        minCost = tmp
    else:
      score = MAP.pop("score")
      DP[tuple(MAP.items())] = 10e9
      MAP["score"] = score
  
  if MAP["score"] + minCost < currentMin:
    currentMin = MAP["score"] + minCost
    #print("New min", currentMin, "len", len(DP))
  
  MAP.pop("score")
  DP[tuple(MAP.items())] = minCost
  return minCost

def mapFromFile(lines):
  MAP = dict()
  for y in range(len(lines)):
    for x in range(len(lines[y])):
      MAP[(x,y)] = (lines[y][x], 0)

  part2Content = ["  #D#C#B#A#", "  #D#B#A#C#"]

  NMAP = dict()
  if part2:
    for m in MAP:
      if m[1] > 2:
        NMAP[(m[0],m[1]+2)] = MAP[m]
        NMAP[m] = (part2Content[m[1]-3][m[0]], 0)
      else:
        NMAP[m] = MAP[m]
  else:
    NMAP = MAP
    
  MAP = NMAP
    
  for m in MAP:
    if m[1] == 1:
      MAP[m] = (MAP[m][0], 1)
    if MAP[m][0] in ["A", "B", "C", "D"]:
      if inGoal(m, MAP):
        MAP[m] = (MAP[m][0], 2)

        
  MAP["score"] = 0
  return  MAP

MAP = mapFromFile(lines)
print("Part1:", solve(MAP))
part2 = True
DP = {}
currentMin = 10e9
MAP = mapFromFile(lines)
print("Part2:", solve(MAP))