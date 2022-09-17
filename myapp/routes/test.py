import datetime as dt
import math

memo = [0] * 1000000
memo[1] = 1

def calc_max(x : int):
    original = x
    mx = x
    while(True):
        if x % 2:
            x = int(x * 3 + 1)
            mx = max(mx, x)
        else:
            x = int(x/2)
            if(x < original):
                return max(mx, memo[x])


my_list = [1,2,3,4,5,6,7,8,9,10]
counter = 0

for x in range(1,100):
    if(memo[x] != 0):
        continue
    mx = calc_max(x)
    memo[x] = mx

print(memo[7])
    
