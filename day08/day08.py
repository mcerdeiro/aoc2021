#!/usr/bin/python3
import copy
from typing import List

lines = open("day08.dat", "r").read().splitlines()

def diff(v1, v2):
  dif = ""
  for v in v1:
    if v not in v2:
      dif += v

  return dif

def getWithLen(vals, length):
  ret = []
  for v in vals:
    if len(v) == length:
      ret.append(v)

  return ret


def getWithAll(vals, withAll):
  ret = []
  for v in vals:
    foundAll = True
    for w in withAll:
      if w not in v:
        foundAll = False
    if foundAll:
      ret.append(v)
  return ret

def getWithoutAnyOf(vals, without):
  ret = []
  for v in vals:
    notPresent = True
    for w in without:
      if w in v:
        notPresent = False
    if notPresent:
      ret.append(v)

  return ret

def getNumbers(vals):
  D = {}
  c,f = "", ""

  for v in vals:
    if len(v) == 2:
      D[1] = v
      D[v] = 1
    if len(v) == 3:
      D[7] = v
      D[v] = 7
    if len(v) == 4:
      D[4] = v
      D[v] = 4
    if len(v) == 7:
      D[8] = v
      D[v] = 8

  a = diff(D[7], D[1])
  possible6 = getWithLen(vals, 6)
  not6 = getWithAll(possible6, D[1])
  for p in possible6:
    if p in not6:
      pass
    else:
      assert(6 not in D.keys())
      D[6] = p
      D[p] = 6

  assert(6 in D.keys())
  c = diff(D[8], D[6])
  f = diff(D[1], c)

  possible235 = getWithLen(vals, 5)
  possible3 = getWithAll(possible235, D[1])
  assert(len(possible3) == 1)
  D[3] = possible3[0]
  D[D[3]] = 3

  possible2 = getWithAll(possible235, c)
  possible2 = getWithoutAnyOf(possible2, f)
  assert(len(possible2) == 1)
  D[2] = possible2[0]
  D[possible2[0]] = 2

  possible5 = getWithAll(possible235, f)
  possible5 = getWithoutAnyOf(possible5, c)
  assert(len(possible5) == 1)
  D[5] = possible5[0]
  D[possible5[0]] = 5

  possible09 = getWithLen(vals, 6)
  possible9 = getWithAll(possible09, D[4])
  assert(len(possible9) == 1)
  D[9] = possible9[0]
  D[possible9[0]] = 9

  possible0 = []
  for p in possible09:
    if p not in D.keys():
      possible0.append(p)

  assert(len(possible0) == 1)
  D[0] = possible0[0]
  D[possible0[0]] = 0

  return D

def find(val, D):
  for k in range(10):
    check = D[k]
    found = True
    if (len(val) == len(check)):
      for c in check:
        if c not in val:
          found = False

      if found == True:
        return k

  assert(0)

p1 = 0
p2 = 0
for line in lines:
  be, af = line.split("|")
  for num in af.split():
    if len(num) in [2, 3, 4, 7]:
      p1 += 1
  D = getNumbers(be.split())
  val = ""
  for v in af.split():
    val += str(find(v, D))
  p2 += int(val)


print("Part1: ", p1)
print("Part2: ", p2)
