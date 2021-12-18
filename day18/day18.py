#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day18.dat", "r").read().splitlines()

gcounter = 0

def recount(vals, firstcall = True):
  global gcounter
  ret = []
  if firstcall == True:
    gcounter = 0
    
  for v in vals:
    if type(v) == list:
      ret.append(recount(v, False))
    else:
      v2 = (v[0], gcounter)
      ret.append(v2)
      gcounter += 1
      
  return ret
  

def processLine(line, firstcall = True):
  val = []
  offset = -1
  for i, v in enumerate(line):
    if offset < 0:
      tmp = []
      if v in ["[", "]", ","]:
        if v in ["["]:
          offset, V = processLine(line[i+1:], False)
          val.append(V)
        if v in ["]"]:
          #print("Return", i, val)
          return i+1, val
      else:
        val.append((int(v), 0))
    else:
      offset -= 1
      if offset == 0:
        offset = -1
      
  if firstcall == True:
    val = recount(val)
    return val
  return i, val

exploded = None
level = 0
def findExploded(L, firstcall = True):
  global level, exploded
  ret = []
  if firstcall:
    exploded = None
    level = -1

  level += 1
  
  if level == 4 and exploded == None:
    if type(L[0]) == list:
      exploded = L[0]
      ret.append((0, None))
      ret.append(L[1])
    elif type(L[1]) == list:
      exploded = L[1]
      ret.append(L[0])
      ret.append((0, None))
    else:
      ret = L
  else:
    for l in L:
      if type(l) == list:
        v = findExploded(l, False)
        ret.append(v)
      else:
        ret.append(l)
    
  level -= 1
  return ret
  
  
replaced = None
def replaceAfter(L, v):
  ret = []
  for l in L:
    if type(l) == list:
      v2 = replaceAfter(l, v)
      ret.append(v2)
    else:
      if l[1] == v[1] + 1:
        ret.append((l[0]+v[0], None))
      else:
        ret.append(l)
    
  return ret

lastFound = 10e9
def findPosBefore(L, v):
  global lastFound
  for l in L:
    if type(l) == list:
      findPosBefore(l, v)
    else:
      print("foo", l, v)
      if l[1] != None:
        if l[1] < v[1]:
          if lastFound == None:
            lastFound = l[1]
          elif l[1] > lastFound:
            lastFound = l[1]
        
  return

def addingBefore(L, pos, v):
  ret = []
  for l in L:
    if type(l) == list:
      ret.append(addingBefore(l, pos, v))
    else:
      if l[1] == pos:
        ret.append((l[0]+v,l[1]))
      else:
        ret.append(l)
      
  return ret

def replaceBefore(L, v):
  global lastFound
  #lastFound = None
  #findPosBefore(L, v)
  #if lastFound != None:
  #print("assert1", L)
  #print("assert2", v[1], v[0])
  L = addingBefore(L, v[1]-1, v[0])
  return L

def uncount(L):
  ret = []
  for l in L:
    if type(l) == list:
      ret.append(uncount(l))
    else:
      ret.append(l[0])
      
  return ret

def tostring(L):
  ret = "["
  
  for i,l in enumerate(L):
    if i == 1:
      ret += ","
    if type(l) == list:
      ret += tostring(l)
    else:
      if type(l) == tuple:
        ret += str(l[0])
      else:
        ret += str(l)
      
  ret += "]"
  
  return ret
  
def process(line):
  L = processLine(line)
  #print("0", uncount(L))
  L = findExploded(L)
  #print("1", uncount(L))
  L = replaceBefore(L, exploded[0])
  #print("2", uncount(L))
  L = replaceAfter(L, exploded[1])
  L = recount(L)
  L = uncount(L)
  L = tostring(L[0])
  #print("Result", L)
  return L

alreadysplit = False
def splitme(L, firstcall = True):
  global alreadysplit
  
  if firstcall:
    alreadysplit = False

  ret = []
  for l in L:
    if type(l) == list:
      ret.append(splitme(l, False))
    else:
      if alreadysplit == False:
        if l[0] >= 10:
          alreadysplit = True
          tmp = []
          tmp.append((l[0]//2, None))
          tmp.append(((l[0]+1)//2, None))
          ret.append(tmp)
        else:
          ret.append(l)
      else:
        ret.append(l)
  return ret

def split(line):
  L = processLine(line)
  print("1", tostring(L[0]))
  L = splitme(L)
  L = recount(L)
  print("2", tostring(L[0]))
  L = tostring(L[0])
  return L

def reduceme(line):
  global exploded
  L = processLine(line)
  #print("Reducing......", tostring(L[0]))
  L2 = None
  
  while L2 != tostring(L[0]):
    L2 = tostring(L[0])
    #print("0", uncount(L))
    explodeagain = True
    while explodeagain:
      explodeagain = False
      beExp = tostring(L[0])
      L = findExploded(L)
      if exploded != None:
        #print("Before Explode", beExp, "explode", exploded[0][0], exploded[1][0])
        explodeagain = True
        #print("1", uncount(L))
        L = replaceBefore(L, exploded[0])
        #print("2", uncount(L))
        L = replaceAfter(L, exploded[1])
        L = recount(L)
        #print("After  Explode", tostring(L[0]))
    L = splitme(L)
    L = recount(L)

  
  
  L = uncount(L)
  L = tostring(L[0])
  #print("Result", L)
  return L


assert(process("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]")
assert(process("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]")
assert(process("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]")
assert(process("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
assert(process("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]")
assert(reduceme("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")

def processMultilines(lines):
  S = None
  for l in lines:
    if S == None:
      S = l
      S = reduceme(S)
    else:
      l = reduceme(l)
      S = "[" + S + "," + l + "]"
      S = reduceme(S)
  return S

def calcMag(L):
  ret = 0
  
  if type(L[0]) == list:
    ret += 3 * calcMag(L[0])
  else:
    ret += 3 * L[0][0]
  
  if type(L[1]) == list:
    ret += 2 * calcMag(L[1])
  else:
    ret += 2 * L[1][0]
    
  return ret

def magnitude(line):
  L = processLine(line)
  return calcMag(L[0])
  

assert(processMultilines(["[1,1]", "[2,2]", "[3,3]", "[4,4]"]) == "[[[[1,1],[2,2]],[3,3]],[4,4]]")
assert(processMultilines(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]"]) == "[[[[3,0],[5,3]],[4,4]],[5,5]]")
assert(processMultilines(["[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]"]) == "[[[[5,0],[7,4]],[5,5]],[6,6]]")
#assert(processMultilines(["[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]"]) == "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]")
assert(magnitude("[[1,2],[[3,4],5]]") == 143)
assert(magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488)

res = processMultilines(lines)
print("Part1", magnitude(res))

p2 = -1000
for i in range(len(lines)):
  for j in range(len(lines)):
    if i != j:
      res = processMultilines((lines[i], lines[j]))
      p2 = max(p2, magnitude(res))

print("Part2", p2)