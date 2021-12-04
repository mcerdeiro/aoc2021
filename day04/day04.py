#!/usr/bin/python3

import copy
from typing import List

class Player:
  
  def __init__(self, data) -> None:
    self._rows = []
    self._matches = set()
    self._countOfPlays = 0  
    self._lastPlayNumer = None
    self._finish: bool = False
    self._score: int = -1
    for line in data:
      tmp = list()
      for v in line.split(" "):
        if v != "":
          tmp.append(int(v))
      self._rows.append(tmp)
      
  def _find(self, val: int) -> tuple():
    for i in range(len(self._rows)):
      for j in range(len(self._rows[i])):
        if self._rows[i][j] == val:
          return i,j
    else:
      return None, None
  
  def _calculateScore(self):
    assert(self._finish)
    val = 0
    for i in range(5):
      for j in range(5):
        if (i,j) in self._matches:
          pass
        else:
          val += self._rows[i][j]
    
    self._score = val * self._lastPlayNumer
    
  
  def _checkWin(self) -> bool:
    for i in range(5):
      found = True
      for j in range(5):
        if (i,j) in self._matches:
          pass
        else:
          found = False
          
      if found == True:
        self._finish = True
        self._calculateScore()
        return self._finish
        
    for i in range(5):
      found = True
      for j in range(5):
        if (j,i) in self._matches:
          pass
        else:
          found = False
          
      if found == True:
        self._finish = True
        self._calculateScore()
        return self._finish
      
    return self._finish
  
  def getScore(self) -> int:
    return self._score
  
  def play(self, number: int) -> bool:
    if self._finish == False:
      self._lastPlayNumer = number
      self._countOfPlays += 1
      x,y = self._find(number)
      if (x != None):
        self._matches.add((x,y))
        return self._checkWin()
    
    return False

  def print(self):
    for i in range(len(self._rows)):
      tmp = ""
      for j in range(len(self._rows[i])):
        space = " "
        if self._rows[i][j] > 9:
          space = ""
        m = " "
        if (i,j) in self._matches:
          m = "*"
        tmp += space + m + str(self._rows[i][j]) + m + "  "
      
      print(tmp)
    print()

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
  first = False
  lines = open(inputfile, "r").read().splitlines()
  players = []
  playersNew: List[Player] = []
  
  values = []
  data = []
  for line in lines:
    if first == False:
      values = [int(x) for x in line.split(",")]
      first = True
    else:
      if line == "":
        if len(data) != 0:
          #print("data", data)
          playersNew.append(Player(data))
          data = []
      else:
        data.append(line)

  playersNew.append(Player(data))
      
  countOfWins = 0
  for v in values:
    for player in playersNew:
      if player.play(v) == True:
        countOfWins += 1
        if (countOfWins == 1):
          print("Part1:", player.getScore())
        elif (countOfWins == len(playersNew)):
          print("Part2:", player.getScore())
          exit()

assert_print(lambda :part1and2("day04.dat"))
