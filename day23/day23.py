#!/usr/bin/python3
import sys
import heapq
import copy

debug = False

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day23.dat", "r").read().splitlines()

def isLateralWayBlocked(fr, to, M):
  assert(fr[1] == 1)
  current = fr
  dir = (current[0]-to[0])/abs(current[0]-to[0])
  current = (current[0]+dir,current[1])
  while M[current][0] == ".":
    if current[0] == to[0]:
      return True
    current = (current[0]+dir,current[1])
  return False

def isImposibleToSolve(M):
  let = []
  level1 = []
  for m in M:
    if M[m][0] in ["A", "B", "C", "D"]:
      let.append(m)
      if m[1] == 1:
        level1.append(m)
  
  blocked = 0
  for l1 in level1:
    if isLateralWayBlocked(l1, getGoal(M[l1][0]), M):
      print("blocked", l1, getGoal(M[l1][0]))
      printMap(M, 10000000, M)
      input()
      blocked += 1

  
  if blocked >= 2:
    return True
  return False
    

def emptyWay(M, fr, to):
  moves = 0
  empty = True
  #assert(fr[1] != to[1])
  if fr[1] == to[1]:
    assert(fr[1] != 1)
  assert(fr[0] != to[0])
  current = fr
  movements = []
  
  if fr[1] == to[1]:
    movements.append("up")
  if fr[1] == 1:
    movements.append("lateral")
  movements.append("down")
  if fr[1] != 1:
    movements.append("lateral")
  if debug:
    print("moves", movements)
  for movement in movements:
    if movement == "up":
      dir = -1
      while current[1] != 1:
        current = (current[0], current[1]+dir)
        moves += 1
        if M[current][0] != ".":
          #print("return1", current)
          return False, moves
    if movement == "lateral":
      dir = (to[0]-fr[0])//abs(to[0]-fr[0])
      while to[0] != current[0]:
        current = (current[0]+dir, current[1])
        moves += 1
        if M[current][0] != ".":
          #print("return2", current)
          return False, moves
    if movement == "down":
      dir = 1
      while to[1] != current[1]:
        current = (current[0], current[1]+dir)
        moves += 1
        if M[current][0] != ".":
          #print("return3", current)
          return False, moves

  return True, moves

def getPosNextMoves(M):
  NM = []
  dest = None
  for m in M:
    if M[m][0] in ["A", "B", "C", "D"] and M[m][1] < 2:
      #if m[1] == 1:
        #todo check if dest empty
      if M[m][0] == "A":
        dest = (3,3)
      elif M[m][0] == "B":
        dest = (5,3)
      elif M[m][0] == "C":
        dest = (7,3)
      elif M[m][0] == "D":
        dest = (9,3)
      else:
        assert(0)
      if M[dest][0] == ".":
        if emptyWay(M, m, dest):
          NM.append(m)
          continue
      if M[dest][0] == M[m][0]:
        if emptyWay(M, m, (dest[0], dest[1]-1)):
          NM.append(m)
          continue
      pass
      if m[1] == 2:
        NM.append(m)
      elif m[1] == 3:
        if M[(m[0],m[1]-1)][0] == ".":
          NM.append(m)
      else:
        if debug:
          print("m", m, M[m])
        #assert(0)

  return NM

def getGoal(let):
  if let == "A":
    return (3, 2)
  elif let == "B":
    return (5, 2)
  elif let == "C":
    return (7, 2)
  elif let == "D":
    return (9, 2)
  
  assert(0)

def calcCost(t, dis):
  mul = 0
  if t == "A":
    mul = 1
  elif t == "B":
    mul = 10
  elif t == "C":
    mul = 100
  elif t == "D":
    mul = 1000
  else:
    assert(0)
  
  if dis*mul == 0:
    if debug:
      print("Type", t, mul, dis)
  assert(dis*mul != 0)
  return dis*mul

def getPosDestinations(pos, M):
  if debug:
    print("Finding dest for", pos, M[pos])
  MOVES = []
  MOVESTOGOAL = []
  if pos[1] in [1,2,3]:
    goal = getGoal(M[pos][0])
    if debug:
      print("Goal", goal, "M at goal", M[goal], "M at goal+1", M[(goal[0],goal[1]+1)])
    if M[(goal[0], goal[1]+1)][0] == ".":
      goal = (goal[0], goal[1]+1)
      way = emptyWay(M, pos, goal)
      #print("Moving from to", pos, goal, "way", way)
      if way[0] != False:
        MOVES.append((goal, calcCost(M[pos][0], way[1])))
        MOVESTOGOAL.append((goal, calcCost(M[pos][0], way[1])))
    elif M[(goal[0], goal[1]+1)][0] == M[pos][0]:
      way = emptyWay(M, pos, goal)
      if debug:
        print("Checkway", pos, goal, way)
      if way[0] != False:
        MOVES.append((goal, calcCost(M[pos][0], way[1])))
        MOVESTOGOAL.append((goal, calcCost(M[pos][0], way[1])))
      pass
    else:
      # not possible to move since destiancion busy
      pass
  if pos[1] == 2:
    for x in range(pos[0], 15):
      if x not in [3,5,7,9]:
        goal = (x,pos[1]-1)
        if M[goal][0] == ".":
          #print("foo", M[pos], M[goal], goal, pos, "dis", abs(goal[0]-pos[0]))
          MOVES.append((goal, \
            calcCost(M[pos][0],1+abs(goal[0]-pos[0]))))
        else:
          break
    for x in range(pos[0], 0, -1):
      if x not in [3,5,7,9]:
        goal = (x,pos[1]-1)
        if M[goal][0] == ".":
          MOVES.append((goal, \
            calcCost(M[pos][0],1+abs(goal[0]-pos[0]))))
        else:
          break
  elif pos[1] == 3:
    if M[pos[0], pos[1]-1][0] == ".":
      for x in range(pos[0], 15):
        if x not in [3,5,7,9]:
          goal = (x,pos[1]-2)
          if M[goal][0] == ".":
            MOVES.append((goal, \
              calcCost(M[pos][0],2+abs(goal[0]-pos[0]))))
          else:
            break
      for x in range(pos[0], 0, -1):
        if x not in [3,5,7,9]:
          goal = (x,pos[1]-2)
          if M[goal][0] == ".":
            MOVES.append((goal, \
              calcCost(M[pos][0],2+abs(goal[0]+pos[0]))))
          else:
            break
  #else:
    #assert(0)
  if len(MOVESTOGOAL) != 0:
    return MOVESTOGOAL
  return MOVES


def checkFinisch(M):
  if M[(3, 2)][0] != "A":
    return False
  if M[(3, 3)][0] != "A":
    return False
  if M[(5, 2)][0] != "B":
    return False
  if M[(5, 3)][0] != "B":
    return False
  if M[(7, 2)][0] != "C":
    return False
  if M[(7, 3)][0] != "C":
    return False
  if M[(9, 2)][0] != "D":
    return False
  if M[(9, 3)][0] != "D":
    return False
  
  return True

def move(fr, to, M):
  M[to] = (M[fr][0], M[fr][1]+1)
  M[fr] = (".", 0)
  

def printMap(M, cost, M2 = None):
  for y in range(5):
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

n = 0
unique = 0
def findShortToOrder():
  global unique, n
  next = heapq.heappop(ways)
  cost, _, M = next
  if debug:
    print("*********** next map *********")
    printMap(M, cost)
  while not checkFinisch(M):
    nextMoves = getPosNextMoves(M)
    if len(nextMoves) > 0:
      if debug:
        print("nextMoves", nextMoves)
      for nm in nextMoves:
        if debug:
          print("nextMove", nm)
        posdests = getPosDestinations(nm, M)
        if debug:
          print("dest", posdests)
        for d in posdests:
          destpoint = d[0]
          newcost = d[1] + cost
          M2 = copy.deepcopy(M)
          move(nm, destpoint, M2)
          # print("new cost", newcost+cost)
          # print("new map", M2)
          # print("ways", len(ways))
          if debug:
            print("Possible new map")
            printMap(M, newcost, M2)
          #input("")
          if isImposibleToSolve(M2) == False:
            heapq.heappush(ways, (newcost, unique, M2))
          else:
            print("Imposible map")
            printMap(M2, 10000000, M2)
            input()
          unique += 1
    
    next = heapq.heappop(ways)
    cost, _, M = next
    if debug:  
      print("*********** next map *********")
      printMap(M, cost)
    else:
      if n > 1000:
        print("*********** next map *********")
        printMap(M, cost)
        n = 0
      n += 1
#    input("wait")
  
  return cost
M = {}
for y in range(len(lines)):
  for x in range(len(lines[y])):
    M[(x,y)] = (lines[y][x], 0)

def correctMoves(M):
  for m in M:
    if M[m][0] in ["A", "B", "C", "D"]:
      if m[1] == 1:
        M[m] = (M[m][0], 1)
      else:
        p = getGoal(M[m][0])
        p = (p[0], p[1]+1)
        if m == p:
          M[m] = (M[m][0], 2)
        else:
          if M[p][0] == M[m][0]:
            p = (p[0], p[1]-1)
            if m == p:
              M[m] = (M[m][0], 2)
      

correctMoves(M)
printMap(M, 0, M)
ways = []
heapq.heappush(ways, (0, 0, M))
print("Part1", findShortToOrder())
