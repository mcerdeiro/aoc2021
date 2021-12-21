#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day21.dat", "r").read().splitlines()

ans1 = 0 
  
p1 = 4
p2 = 8

def move(pos, moves):
  res = pos + moves
  while res > 10:
    res -= 10
  return res
  

class Game:
  def __init__(self, p1, p2, goal):
    self.p1 = p1
    self.p2 = p2
    self.p1score = 0
    self.p2score = 0
    self.rolls = 0
    self.turn = 0
    self.result = 0
    self.goal = goal
    self.next = 1

  def roll(self,count):
    if self.turn % 6 < 3:
      self.p1 += count
      while self.p1 > 10:
        self.p1 -= 10
    else:
      self.p2 += count
      while self.p2 > 10:
        self.p2 -= 10
      
    if self.turn % 6 == 2:
      self.p1score += self.p1
      self.next = 2
    if self.turn % 6 == 5:
      self.p2score += self.p2
      self.next = 1
    
    self.rolls += 1
    self.turn += 1
  
    if self.p1score >= self.goal:
      self.result = self.p2score * self.rolls
      return "p1"
    if self.p2score >= self.goal:
      self.result = self.p1score * self.rolls
      return "p2"
    return None


play = Game(4,8, 1000)
roll = 1
for i in range(1000):
  if play.roll(roll) != None:
    print("Part 1:", play.result)
    break
  roll += 1
  if roll > 100:
    roll = 1

STORE = {}

def playmultiuniverse(game):
  assert(game.result == 0)
  myplay = (game.p1, game.p2, game.p1score, game.p2score, game.next)
  if myplay in STORE:
    return STORE[myplay]

  ans = (0,0)
  
  for r1 in range(3):
    for r2 in range(3):
      for r3 in range(3):
        p = copy.deepcopy(game)
        r = p.roll(r1+1)
        assert(r == None)
        r = p.roll(r2+1)
        assert(r == None)
        r = p.roll(r3+1)
        if r == None:
          an = playmultiuniverse(p)
          ans = (ans[0]+an[0], ans[1]+an[1])
        elif r == "p1":
          ans = (ans[0]+1,ans[1])
        elif r == "p2":
          ans = (ans[0],ans[1]+1)
        else:
          assert(0)
  
  STORE[myplay] = ans
  return ans


GOAL = 21
myplay = Game(7,3,GOAL)
res = playmultiuniverse(myplay)
print("Part 2:", max(res))