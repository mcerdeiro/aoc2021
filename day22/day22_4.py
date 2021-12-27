#!/usr/bin/python3
from abc import abstractproperty
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day22.dat", "r").read().splitlines()

def currentlyOn(R):
  ans1 = 0
  for r in R:
    if R[r] == 1:
      ans1 += 1
  return ans1

def getCountCubes(p):
  x = 0
  y = 0
  z = 0
  x = abs(p[0][0]-p[0][1])+1
  y = abs(p[1][0]-p[1][1])+1
  z = abs(p[2][0]-p[2][1])+1
  return x*y*z

D = []
for line in lines:
  if "#" in line:
    continue
  on = False
  if "on" in line:
    on = True
  
  x = line.split("x=")[1].split(",y")[0]
  y = line.split("x=")[1].split(",y=")[1].split(",z=")[0]
  z = line.split("x=")[1].split(",y=")[1].split(",z=")[1]
  x1, x2 = [int(a) for a in x.split("..")]
  y1, y2 = [int(b) for b in y.split("..")]
  z1, z2 = [int(c) for c in z.split("..")]

  p = ((x1,x2), (y1, y2), (z1, z2))
  D.append((p, on))
    
def sameRange(x, x1):
  if x1[0] <= x[0] <= x1[1]:
    return True
  if x1[0] <= x[1] <= x1[1]:
    return True
  if x[0] <= x1[0] <= x[1]:
    return True
  if x[0] <= x1[1] <= x[1]:
    return True
  
  return False

def hasIntersection(p1, p2):
  if sameRange(p1[0], p2[0]):
    if sameRange(p1[1], p2[1]):
      if sameRange(p1[2], p2[2]):
        return True
  return False

def getInside(r1, r2):
  return (max(r1[0], r2[0]), min(r1[1], r2[1]))

def getOutside(r1, r2):
  outside = []
  if r1[0] < r2[0]:
    outside.append((r1[0], r2[0]-1))
  if r1[1] > r2[1]:
    outside.append((r2[1]+1, r1[1]))
  
  return outside

def getOutsides(r1, r2):
  outx = getOutside(r1[0], r2[0])
  outy = getOutside(r1[1], r2[1])
  outz = getOutside(r1[2], r2[2])
  
  assert(len(outx) < 3)
  assert(len(outy) < 3)
  assert(len(outz) < 3)
  return outx, outy, outz

def getInsides(r1, r2):
  inx = getInside(r1[0], r2[0])
  iny = getInside(r1[1], r2[1])
  inz = getInside(r1[2], r2[2])
  
  return inx, iny, inz

def removeOffs(group, OFF):
  print("Processing group", group)
  result = [group]
  inoff = False
  for off in OFF:
    nexttoprocess = []  
    inoff = True
    for process in result:
      if hasIntersection(process[0], off[0]):
        nexttoprocess += getOutsideGroups(process[0], off[0])
      else:
        print("Nointersection", process)
        print("Before", nexttoprocess)
        nexttoprocess.append(process)
        print("After", nexttoprocess)
    result = nexttoprocess

  return result

def countOnOffIntersections(groups:list):
  OFF = []
  for i,group in enumerate(groups):
    if group[1] == False:
      OFF.append((i, group))
      
  groupswithoutoff = []
  
  for i, group in enumerate(groups):
    if group[1] == False:
      continue
    offswithintersection = []
    for off in OFF:
      if off[0] > i:
        if hasIntersection(group[0], off[1][0]):
          offswithintersection.append(off[1])
    if len(offswithintersection) > 0:
      withoutoffs = removeOffs(group, offswithintersection)
      print("*******************Adding here1", withoutoffs)
      groupswithoutoff += withoutoffs
    else:
      print("*******************Adding here2", group)
      groupswithoutoff.append(group)
      
    # # only for on groups
    # if group[1] == True:
    #   print("Processing group", i, group)
    #   toprocess = [group]
    #   nexttoprocess = []
    #   inoff = False
    #   for off in OFF:
    #     if i < off[0]:
    #       inoff = True
    #       for process in toprocess:
    #         #off apply to this group
    #         if hasIntersection(process[0], off[1][0]):
    #           print("Has intersection with off", group[0], "off", off[1])
    #           nexttoprocess += getOutsideGroups(process[0], off[1][0])
    #     toprocess = nexttoprocess
    #   if inoff == False:
    #     toprocess.append(group)
    #   groupswithoutoff += toprocess
    #   print("Result", toprocess)
    # else:
    #   #print("ignore off", group)
    #   pass

  print("After off")
  for gwo in groupswithoutoff:
    print("**", gwo)
  
  return countOnIntersections(groupswithoutoff)

def getOutsideGroups(range, outrange):
  newtoadd = []
  outx, outy, outz = [None, None, None]
  outx, outy, outz = getOutsides(range, outrange)
  taon = True
  # else:
  #   outx, outy, outz = getInsides(tarange, orange)
  # #print("Outsides x", outx, "y", outy, "z", outz)
  
  xrange = None
  if len(outx) > 0:
    xrange = getOutside(range[0], outx[0])
    assert(len(xrange) == 1)
    if len(outx) == 2:
      xrange = getOutside(xrange[0], outx[1])
    assert(len(xrange) == 1)
    #print("xrange", xrange)
    xrange = xrange[0]
  else:
    xrange = range[0]
  
  yrange = None
  if len(outy) > 0:
    yrange = getOutside(range[1], outy[0])
    #print("getOutside from", range[1], outy[0], "returned", yrange)
    assert(len(yrange) == 1)
    if len(outy) == 2:
      yrange = getOutside(yrange[0], outy[1])
    assert(len(yrange) == 1)
    #print("yrange", yrange)
    yrange = yrange[0]
  else:
    yrange = range[1]
  
  zrange = None
  if len(outz) > 0:
    zrange = getOutside(range[2], outz[0])
    assert(len(zrange) == 1)
    if len(outz) == 2:
      zrange = getOutside(zrange[0], outz[1])
    assert(len(zrange) == 1)
    #print("zrange", zrange)
    zrange = zrange[0]
  else:
    zrange = range[2]
    
  #print("Adding", outx, outy, outz, xrange, yrange, zrange)
  
  for ox in outx:
    newtoadd.append(((ox, yrange, zrange), taon))
    
  for oy in outy:
    newtoadd.append(((xrange, oy, zrange), taon))
  
  for oz in outz:
    newtoadd.append(((xrange, yrange, oz), taon))
    
  if len(outy) > 0 and len(outz) > 0 and len(outx) > 0:
    for ox in outx:
      for oy in outy:
        for oz in outz:
          newtoadd.append(((ox, oy, oz), taon))
  if len(outx) > 0 and len(outy) > 0:
    for ox in outx:
      for oy in outy:
        newtoadd.append(((ox, oy, zrange), taon))
  if len(outx) > 0 and len(outz) > 0:
    for ox in outx:
      for oz in outz:
        newtoadd.append(((ox, yrange, oz), taon))
  if len(outy) > 0 and len(outz) > 0:
    for oy in outy:
      for oz in outz:
        newtoadd.append(((xrange, oy, oz), taon))

  return newtoadd

def countOnIntersections(groups):
  PROCESSED = []
  result = 0

  for group in groups:
    toadd = [group]
    newtoadd = []
    
    for processed in PROCESSED:
      newtoadd = []
      for ta in toadd:
        orange, oon = processed
        tarange, taon = ta
        if hasIntersection(tarange, orange):
          newtoadd += getOutsideGroups(tarange, orange)
        else:
          newtoadd.append(ta)
      toadd = newtoadd
    
    newcubes = 0
    for r in toadd:
      n = getCountCubes(r[0])
      newcubes += n
    result += newcubes

    PROCESSED.append(group)
  
  return result

ans2 = 0
OLD = []

@DeprecationWarning
def remove(OLD, toremove):
  print("Removing", toremove)
  count = 0
  OLDINSIDE = []
  for old in OLD:
    OLDINSIDE.append(getInsides(toremove, old[0]))
    
  print("Removing", toremove, OLDINSIDE)
  #exit()

R = {}
ON = []
ans2 = 0
new = 0
for d in D:
  on = d[1]
  x1, x2 = d[0][0]
  y1, y2 = d[0][1]
  z1, z2 = d[0][2]
  # for x in range(x1, x2+1):
  #   for y in range(y1, y2+1):
  #     for z in range(z1, z2+1):
  #       if on:
  #         R[(x,y,z)] = 1
  #       else:
  #         R[(x,y,z)] = 0
          
  # new = currentlyOn(R)

ans2 = countOnOffIntersections(D)
print("countOnOffIntersections(D)", ans2)
print("Manual", new)
assert(new == ans2)

    