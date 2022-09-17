import logging
import json
import math

from flask import request, jsonify
from myapp import app

logger = logging.getLogger(__name__)

memo = [0] * 1000000

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    result = []
    for xs in data:
        buf = []
        for x in xs:
            if x in memo:
                buf.append(memo[x])
            else:
                y = int(calc_max(x))
                memo[x] = y
                buf.append(y)
        result.append(buf)
    return jsonify(result)

@app.route('/cryptocollapztest', methods=['GET'])
def cryptocollapztest():
    data = [[1,2,3,4], [1,2,3,4]]
    result = []
    memo = {}
    for tc in data:
        tc_out = []
        for i in tc:
            start = i
            max = i
            while i != 1:
                if i % 2 != 0:
                    i = i * 3 + 1
                    if i in memo.keys():
                        max = memo[i]
                        break
                    if i > max:
                        max = i
                i /= 2
            memo[start] = max
            tc_out.append(max)
        result.append(tc_out)
    return jsonify(result)


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

# def calc_max(x : int):
#     mx = max(x, 4)
#     buf = [x]
#     n = math.log2(x)
#     if(n == int(n)):
#         return x
#
#     r = x - int(n) # x = 2^n + r
#     return r
#
#
#     while(True):
#         if(x == 1):
#             break
#         if(x % 2 == 0):
#             x /= 2
#         else:
#             x = x * 3 + 1
#         mx = max(mx, x)
#         buf.append(x)
#         count += 1
#     return int(mx)
#          
#
