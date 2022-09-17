
import json

from flask import request, jsonify
from collections import defaultdict
from myapp import app

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    stream = data
    const result = []
    for tc in stream:
        buf = []
        for(i in range(len(tc))):
            buf.append(calc_max(tc[i]))
        result.append(buf) 

    return result

def calc_max(x : int):
    mx = x
    while(True):
        if(x == 1): break
        if(x % 2 == 0):
            x /= 2
        else:
            x = x * 3 + 1
        mx = max(mx, x)
    return int(mx)
         

