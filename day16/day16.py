#!/usr/bin/python3
import copy
from typing import DefaultDict, List
import sys
from collections import defaultdict
import heapq

lines = open(sys.argv[1] if len(sys.argv) > 1 else "day16.dat", "r").read().splitlines()

MAP = {0: "sum", 1: "product", 2: "min", 3: "max", 5: ">", 6: "<", 7: "=="}

p1 = 0

def adapt(line):
  tmp = ""
  for el in line:
    val = str(bin(int(el,16)))
    rest = 4 - len(val[2:])
    for i in range(rest):
      tmp += "0"
    tmp += str(val[2:])
  return tmp
  
  
def process(packet):
  global p1
  pos = 0
  version = int(packet[pos:pos+3],2)  
  p1 += version
  value =  0
  
  pos += 3
  packtype = int(packet[pos:pos+3],2)
  pos +=3
  if packtype == 4:
    val = ""
    cont = True
    while cont:
      cont = (packet[pos] == "1")
      pos += 1
      val += packet[pos:pos+4]
      pos += 4
    value = int(val,2)
    return pos, value
  else:
    
    I = int(packet[pos:pos+1],2)
    pos+=1
    lenghtL = 11
    if (I==0):
      lenghtL = 15

    L = int(packet[pos:pos+lenghtL],2)
    pos += lenghtL
    values = []
    posstart = pos
    while True:
      p, v = process(packet[pos:])
      pos += p
      values.append(v)
      #print("p1", p1)
      #print("Current pos", pos)
      if I == 1:
        if len(values) == L:
          break
      if I == 0:
        print("Check", pos-posstart, L)
        if pos-posstart == L:
           break
      
    
    if packtype == 0:
      value = sum(values)
    elif packtype == 1:
      #print("Values", values, "operation", MAP[packtype], packtype, "=", value, "lenght", L, "in", "count" if I == 1 else "bits")
      #assert(len(values) == 2)
      value = 1
      for v in values:
        value *= v
    elif packtype == 2:
      value = min(values)
    elif packtype == 3:
      value = max(values)
    elif packtype == 5:
      assert(len(values) == 2)
      value = (values[0] > values[1])
    elif packtype == 6:
      assert(len(values) == 2)
      value = (values[0] < values[1])
    elif packtype == 7:
      assert(len(values) == 2)
      value = (values[0] == values[1])
    else:
      assert(0)
      
    print("Values", values, "operation", MAP[packtype], packtype, "=", value, "lenght", L, "in", "count" if I == 1 else "bits")
    #assert(len(values) == 2)
    
    return pos, value
  

p,v = process(adapt("D2FE28"))
assert(v == 2021)  
p,v = process(adapt("38006F45291200"))
assert(v == True) 
p,v = process(adapt("C200B40A82"))
assert(v == 3)
p,v = process(adapt("04005AC33890"))
assert(v == 54)
p,v = process(adapt("880086C3E88112"))
assert(v == 7)
p,v = process(adapt("CE00C43D881120"))
assert(v == 9)
p,v = process(adapt("D8005AC2A8F0"))
assert(v == True)
p,v = process(adapt("F600BC2D8F"))
assert(v == 0)
p,v = process(adapt("9C005AC2F8F0"))
assert(v == 0)
p,v = process(adapt("9C0141080250320F1802104A08"))
assert(v == 1)


print("Test ENDS")
#p,v = process(adapt("C200B40A82"))
#assert(v == 3)  
# p,v = process(adapt("04005AC33890"))
# assert(v == 54)
# p,v = process(adapt("880086C3E88112"))
# assert(v == 7)

line = adapt(lines[0])
print("line", line)
print(process(line))
exit()

print(tmp)
version = int(tmp[0:3],2)
print("version", version)
pid = int(tmp[3:6],2)
print("pid", pid)

I = int(tmp[6:7],2)
print(I)

cur = 7
lenghtL = 11
if (I==0):
  lenghtL = 15

L = int(tmp[cur:cur+lenghtL],2)
print(L)

cur += lenghtL

  