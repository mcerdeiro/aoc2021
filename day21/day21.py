#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day21.dat", "r").read().splitlines()

class Game:
  def __init__(self, posplayer1: int, posplayer2: int, goal: int):
    self.posplayer1 = posplayer1
    self.posplayer2 = posplayer2
    self.scoreplayer1 = 0
    self.scoreplayer2 = 0
    self.totalrolls = 0
    self.result = 0
    self.goal = goal

  def getNextPlayer(self):
    if self.totalrolls % 6 < 3:
      return 1
    return 2
  
  def getState(self):
    assert((self.totalrolls % 6) in [0, 3])
    return self.posplayer1, self.posplayer2, self.scoreplayer1, self.scoreplayer2, self.getNextPlayer()
  
  def copy(self):
    newgame = Game(self.posplayer1, self.posplayer2, self.goal)
    newgame.scoreplayer1 = self.scoreplayer1
    newgame.scoreplayer2 = self.scoreplayer2
    newgame.totalrolls = self.totalrolls
    return newgame

  def move(self, count: int):
    if self.totalrolls % 6 < 3:
      self.posplayer1 += count
      while self.posplayer1 > 10:
        self.posplayer1 -= 10
    else:
      self.posplayer2 += count
      while self.posplayer2 > 10:
        self.posplayer2 -= 10
      
    if self.totalrolls % 6 == 2:
      self.scoreplayer1 += self.posplayer1
    if self.totalrolls % 6 == 5:
      self.scoreplayer2 += self.posplayer2
    
    self.totalrolls += 1
  
    if self.scoreplayer1 >= self.goal:
      self.result = self.scoreplayer2 * self.totalrolls
      return "p1"
    if self.scoreplayer2 >= self.goal:
      self.result = self.scoreplayer1 * self.totalrolls
      return "p2"
    return None

posplayer1 = None
posplayer2 = None
for line in lines:
  if "starting position: " in line:
    if posplayer1 == None:
      posplayer1 = int(line.split("starting position: ")[1])
    else:
      posplayer2 = int(line.split("starting position: ")[1])


play = Game(posplayer1, posplayer2, 1000)
roll = 1
for i in range(1000):
  if play.move(roll) != None:
    print("Part 1:", play.result)
    break
  roll += 1
  if roll > 100:
     roll = 1

STORE = {}

def playmultiuniverse(game: Game):
  assert(game.result == 0)
  gamestate = game.getState()
  if gamestate in STORE:
    return STORE[gamestate]

  ans = (0,0)
  
  for r1 in range(3):
    for r2 in range(3):
      for r3 in range(3):
        newgame = game.copy()
        r = newgame.move(r1+1)
        assert(r == None)
        r = newgame.move(r2+1)
        assert(r == None)
        r = newgame.move(r3+1)
        if r == None:
          an = playmultiuniverse(newgame)
          ans = (ans[0]+an[0], ans[1]+an[1])
        elif r == "p1":
          ans = (ans[0]+1,ans[1])
        elif r == "p2":
          ans = (ans[0],ans[1]+1)
        else:
          assert(0)
  
  STORE[gamestate] = ans
  return ans


GOAL = 21
game = Game(posplayer1, posplayer2, GOAL)
res = playmultiuniverse(game)
print("Part 2:", max(res))