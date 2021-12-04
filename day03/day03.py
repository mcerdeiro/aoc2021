#!/usr/bin/python3

import copy

p1 = 0
p2 = 0
lines = open("day03.dat", "r").read().splitlines()


com = []
nocom = []
for i in range(len(lines[0])):
  c0 = 0
  c1 = 0
  for line in lines:
    if line[i] == "1":
      c1 += 1
    if line[i] == "0":
      c0 += 1
      
  if (c1 > c0):
    com.append("0")
    nocom.append("1")
  elif (c1 < c0):
    com.append("1")
    nocom.append("0")
  else:
    print(i, c1, c0)
    assert(0)
    
val = int("".join(com), 2)
val2 = int("".join(nocom), 2)
print("Part1:", val2*val)
    

#print("Part2: ", p2)

def mostCommon(vals, pos):
  c0 = 0
  c1 = 0
  for val in vals:
    if val[pos] == "0":
      c0 += 1
    elif val[pos] == "1":
      c1 += 1
    else:
      assert(0)
  return c1, c0

all = copy.deepcopy(lines)
tmp = []

t1 = 0
while len(all) > 1:
  for i in range(len(all[0])):
    #print("checking pos", i)
    c1, c0 = mostCommon(all, i)
    search = ""
    if c1 >= c0:
      search = "1"
    else:
      search = "0"
    for v in all:
      if v[i] == search:
        tmp.append(v)
    
    all = copy.deepcopy(tmp)
    tmp = []
    #print("Length", len(all))
    if len(all) == 1:
      t1 = int(all[0],2)
      break
    
      
      
all = copy.deepcopy(lines)
while len(all) > 1:
  for i in range(len(all[0])):
    #print("checking pos", i)
    c1, c0 = mostCommon(all, i)
    search = ""
    if c1 >= c0:
      search = "0"
    else:
      search = "1"
    for v in all:
      if v[i] == search:
        tmp.append(v)
    
    all = copy.deepcopy(tmp)
    tmp = []
    #print("Length", len(all))
    if len(all) == 1:
      print("Part2:", int(all[0],2) * t1)
      break
      
  
  
  
  
