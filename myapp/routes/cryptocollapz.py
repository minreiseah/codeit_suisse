import logging
import json
import math

from flask import request, jsonify
from myapp import app

logger = logging.getLogger(__name__)

memo = [0] * 10000000
memo[1] = 4

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    result = []
    logging.info(data)
    for xs in data:
        buf = []
        for x in xs:
            if(memo[x] != 0):
                buf.append(memo[x])
            else:
                mx = calc_max(x)
                memo[x] = mx
                buf.append(mx)
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


def calc_max(x: int):
    mx = x
    while (True):
        if x % 2:
            x = int(x * 3 + 1)
            mx = max(mx, x)
        else:
            x = int(x / 2)
            if x in memo:
                return max(mx, memo[x])


# data = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
#
# result = []
# for xs in data:
#     buf = []
#     for x in xs:
#         if (memo[x] != 0):
#             buf.append(memo[x])
#         else:
#             mx = calc_max(x)
#             memo[x] = mx
#             buf.append(mx)
#     result.append(buf)
#
# print(calc_max(7))
