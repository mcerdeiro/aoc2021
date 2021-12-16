#!/usr/bin/python3
import copy
from os import device_encoding
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day16.dat", "r").read().splitlines()

MAP = {0: "sum", 1: "product", 2: "min", 3: "max", 5: ">", 6: "<", 7: "=="}

p1 = 0

def toBinaryString(line):
  tmp = ""
  for el in line:
    val = str(bin(int(el,16)))
    rest = 4 - len(val[2:])
    for i in range(rest):
      tmp += "0"
    tmp += str(val[2:])
  return tmp

def readBits(packet, length):
  return int(packet[0:length],2)

def readVersion(packet):
  return readBits(packet, 3)

def readPackedIdType(packet):
  return readBits(packet[3:], 3)

def getVal(packet):
  offset = 0
  value = ""
  cont = True
  while cont:
    cont = (packet[offset] == "1")
    offset += 1
    value += packet[offset:offset+4]
    offset += 4
  return offset, int(value,2)
    

def process(packet):
  global p1
  offset = 0
  
  VERSION = readVersion(packet)
  p1 += VERSION
  PTID = readPackedIdType(packet)
  
  offset += 6
  RESULT =  0

  if PTID == 4:
    o, RESULT = getVal(packet[offset:])
    offset += o
    return offset, RESULT
  else:
    LENGTHTYPEID = packet[offset:offset+1] == "1"
    offset+=1
    lenghtL = 11
    if (LENGTHTYPEID==0):
      lenghtL = 15

    L = readBits(packet[offset:], lenghtL)
    offset += lenghtL
    
    
    
    values = []
    posstart = offset
    
    
    while True:
      p, v = process(packet[offset:])
      offset += p
      values.append(v)
      if LENGTHTYPEID == 1:
        if len(values) == L:
          break
      if LENGTHTYPEID == 0:
        if offset-posstart == L:
           break
      
    
    if PTID == 0:
      RESULT = sum(values)
    elif PTID == 1:
      RESULT = 1
      for v in values:
        RESULT *= v
    elif PTID == 2:
      RESULT = min(values)
    elif PTID == 3:
      RESULT = max(values)
    elif PTID == 5:
      assert(len(values) == 2)
      RESULT = (values[0] > values[1])
    elif PTID == 6:
      assert(len(values) == 2)
      RESULT = (values[0] < values[1])
    elif PTID == 7:
      assert(len(values) == 2)
      RESULT = (values[0] == values[1])
    else:
      assert(0)
    
    return offset, RESULT
  

assert(toBinaryString("D2FE28")=="110100101111111000101000")
assert(toBinaryString("38006F45291200")=="00111000000000000110111101000101001010010001001000000000")
assert(toBinaryString("EE00D40C823060")=="11101110000000001101010000001100100000100011000001100000")

p,v = process(toBinaryString("D2FE28"))
assert(v == 2021)  
p,v = process(toBinaryString("38006F45291200"))
assert(v == True) 
p,v = process(toBinaryString("C200B40A82"))
assert(v == 3)
p,v = process(toBinaryString("04005AC33890"))
assert(v == 54)
p,v = process(toBinaryString("880086C3E88112"))
assert(v == 7)
p,v = process(toBinaryString("CE00C43D881120"))
assert(v == 9)
p,v = process(toBinaryString("D8005AC2A8F0"))
assert(v == True)
p,v = process(toBinaryString("F600BC2D8F"))
assert(v == 0)
p,v = process(toBinaryString("9C005AC2F8F0"))
assert(v == 0)
p,v = process(toBinaryString("9C0141080250320F1802104A08"))
assert(v == 1)

line = toBinaryString(lines[0])
p1 = 0
_, v = process(line)
print("Part1:", p1)
print("Part2:", v)
