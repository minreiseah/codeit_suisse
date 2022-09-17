import datetime as dt
import math

memo = [0] * 1000000

def calc_max(x : int):
    n = math.log2(x)
    if(n == int(n)):
        return x

    if(memo[x] != 0):
        return memo[x]

    if(x % 2 == 0): #even
        x = int (x/2)
    else:
        x = int (3 * x + 1)

    return max(x, calc_max(x))


my_list = [1,2,3,4,5,6,7,8,9,10]

for x in my_list:
    if x in memo:
        print(memo[x])
    else:
        y = int(calc_max(x))
        memo[x] = y
        print(y)
    
print(memo[:10])
