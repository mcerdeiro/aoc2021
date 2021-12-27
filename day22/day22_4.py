#!/usr/bin/python3
from abc import abstractproperty
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day22.dat", "r").read().splitlines()

def getCountCubes(p):
  x = 0
  y = 0
  z = 0
  x = abs(p[0][0]-p[0][1])+1
  y = abs(p[1][0]-p[1][1])+1
  z = abs(p[2][0]-p[2][1])+1
  return x*y*z
   
def overlap(x, x1):
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
  if overlap(p1[0], p2[0]):
    if overlap(p1[1], p2[1]):
      if overlap(p1[2], p2[2]):
        return True
  return False

def getInsideForOneCoordinate(r1, r2):
  return (max(r1[0], r2[0]), min(r1[1], r2[1]))

def getOutsideForOneCoordinate(r1, r2):
  outside = []
  if r1[0] < r2[0]:
    outside.append((r1[0], r2[0]-1))
  if r1[1] > r2[1]:
    outside.append((r2[1]+1, r1[1]))
  
  return outside

def getOutside(r1, r2):
  outx = getOutsideForOneCoordinate(r1[0], r2[0])
  outy = getOutsideForOneCoordinate(r1[1], r2[1])
  outz = getOutsideForOneCoordinate(r1[2], r2[2])
  
  assert(len(outx) < 3)
  assert(len(outy) < 3)
  assert(len(outz) < 3)
  return outx, outy, outz

def getInside(r1, r2):
  inx = getInsideForOneCoordinate(r1[0], r2[0])
  iny = getInsideForOneCoordinate(r1[1], r2[1])
  inz = getInsideForOneCoordinate(r1[2], r2[2])
  
  return inx, iny, inz

def removeOffs(group, OFF):
  result = [group]
  for off in OFF:
    nexttoprocess = []  
    for process in result:
      if hasIntersection(process[0], off[0]):
        nexttoprocess += getOutsideGroups(process[0], off[0])
      else:
        nexttoprocess.append(process)
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
      groupswithoutoff += withoutoffs
    else:
      groupswithoutoff.append(group)
          
  
  return countOnIntersections(groupswithoutoff)

def getOutsideGroups(range, outrange):
  newtoadd = []
  outx, outy, outz = [None, None, None]
  outx, outy, outz = getOutside(range, outrange)
  taon = True
  
  xrange = None
  if len(outx) > 0:
    xrange = getOutsideForOneCoordinate(range[0], outx[0])
    assert(len(xrange) == 1)
    if len(outx) == 2:
      xrange = getOutsideForOneCoordinate(xrange[0], outx[1])
    assert(len(xrange) == 1)
    #print("xrange", xrange)
    xrange = xrange[0]
  else:
    xrange = range[0]
  
  yrange = None
  if len(outy) > 0:
    yrange = getOutsideForOneCoordinate(range[1], outy[0])
    #print("getOutside from", range[1], outy[0], "returned", yrange)
    assert(len(yrange) == 1)
    if len(outy) == 2:
      yrange = getOutsideForOneCoordinate(yrange[0], outy[1])
    assert(len(yrange) == 1)
    #print("yrange", yrange)
    yrange = yrange[0]
  else:
    yrange = range[1]
  
  zrange = None
  if len(outz) > 0:
    zrange = getOutsideForOneCoordinate(range[2], outz[0])
    assert(len(zrange) == 1)
    if len(outz) == 2:
      zrange = getOutsideForOneCoordinate(zrange[0], outz[1])
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
  
ans2 = countOnOffIntersections(D)
print("Part2:", ans2)

    