import logging
import json

from flask import request, jsonify
from myapp import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    result = []
    for tc in data:
        buf = []
        for i in range(len(tc)):
            buf.append(calc_max(tc[i]))
        result.append(buf) 

    return jsonify(result)

@app.route('/cryptocollapztest', methods=['GET'])
def cryptocollapztest():
    stream = [[1,2,3,4], [1,2,3,4]]
    result = []
    for tc in stream:
        buf = []
        for i in range(len(tc)):
            buf.append(calc_max(tc[i]))
        result.append(buf) 

    return jsonify(result)

def calc_max(x : int):
    mx = max(x, 4)
    buf = [x]
    count = 0
    while(True):
        if(x in buf[:-2] or count == 100): break
        if(x % 2 == 0):
            x /= 2
        else:
            x = x * 3 + 1
        mx = max(mx, x)
        buf.append(x)
        count += 1
    return int(mx)
         

