import logging
import json

from flask import request, jsonify
from myapp import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    result = []
    memo = {}
    for tc in data:
        tc_out = []
        for i in tc:
            start = i
            max = i
            counter = 0
            while i != 1 or counter > 524:
                counter += 1
                if i in memo.keys():
                    max = memo[i]
                    break
                if i % 2 != 0:
                    i = i * 3 + 1
                    if i > max:
                        max = i
                i /= 2
            memo[start] = max
            tc_out.append(max)
        result.append(tc_out)
    return jsonify(result)

@app.route('/cryptocollapztest', methods=['GET'])
def cryptocollapztest():
    stream = [[1,2,3,4], [1,2,3,4]]
    result = []
    for tc in stream:
        tc_result = []
        for i in tc:
            max = i
            while i != 1:
                if i % 2 != 0:
                    i = i * 3 + 1
                    if i > max:
                        max = i
                i /= 2
            tc_result.append(max)
        result.append(tc_result) 
    return jsonify(result)

def calc_max(x : int):
    mx = max(x, 4)
    buf = [x]
    count = 0
    while(True):
        if(x == 1 or count == 100):
            break
        if(x % 2 == 0):
            x /= 2
        else:
            x = x * 3 + 1
        mx = max(mx, x)
        buf.append(x)
        count += 1
    return int(mx)
         

