
import math

def areacircle(c):
   d = []
   e=0
   for i in range(c):
        a=i+1
        b = math.pi * (a*a)
        d.append(b)
   d.pop(0)
   d.append(10)
   for i in d:
       e=e+i
   print(e)
    

val = input("Enter radius: ")

areacircle(int(val))
