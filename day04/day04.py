#!/usr/bin/python3
import copy

def assert_print(func, expected = None):
  val = func()
  if expected == None:
    print("Result:", val)
  else:
    if val == expected:
      print("OK", val)
    else:
      print("FAILED expected", expected, "returned", val)



def processFirst(line):
  vals = [int(x) for x in line.split(",")]
  return vals

def processPlayer(data):
  d = []
  for line in data:
    tmp = []
    for v in line.split(" "):
      if v != "":
        tmp.append(int(v))
    d.append(tmp)
  
  return d

def contains(player, value):
  for i in range(len(player)):
    for j in range(len(player[1])):
      if player[i][j] == value:
        return i,j
  else:
    return None, None
  
def checkWin(match):
  for i in range(5):
    found = True
    for j in range(5):
      if (i,j) in match:
        pass
      else:
        found = False
        
    if found == True:
      print(i, "H")
      print("Winns hor")
      return i, "H"
      
  for i in range(5):
    found = True
    for j in range(5):
      if (j,i) in match:
        pass
      else:
        found = False
        
    if found == True:
      print(j, "V")
      print("Winns ver")
      return j, "V"
      
      
  return -1, "-"

def printGame(player, match):
  for i in range(len(player)):
    tmp = ""
    for j in range(len(player[i])):
      space = " "
      if player[i][j] > 9:
        space = ""
      m = " "
      if (i,j) in match:
        m = "*"
      tmp += space + m + str(player[i][j]) + m + "  "
      
    print(tmp)
  print()

def play(player, values, count):
  print("Player", player, "Turn", count)
  print("Values", values[0:count])
  match = set()
  win = False
  for i in range(count):
    x,y = contains(player, values[i])
    if x != None:
      match.add((x,y))
  
  printGame(player, match)
      
  c, d = checkWin(match)
  if (c >= 0):
    val = 0
    for i in range(5):
      for j in range(5):
        if (i,j) in match:
          pass
        else:
          val += player[i][j]
        
    print(val, values[count-1])
    print("Part1", values[count-1]*val)
    exit()
      
  
    
    
  
    
  
  

def part1(inputfile):
  first = False
  lines = open(inputfile, "r").read().splitlines()
  players = []
  
  values = []
  data = []
  for line in lines:
    if first == False:
      values = processFirst(line)
      first = True
    else:
      if line == "":
        print("data", data)
        players.append(processPlayer(data))
        data = []
      else:
        data.append(line)
        
    
  print("values", values)
  print("players", players)
  for i in range(len(values)):
    for player in players:
      play(player, values, i)
    
    
    
    
  return 1



#assert_print(lambda :part1("ex01.dat"), 188)
assert_print(lambda :part1("day04.dat"))
