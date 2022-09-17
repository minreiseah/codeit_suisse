import logging
import json

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)

@app.route('/magiccauldrons', methods=['POST'])
def magiccauldrons():
    data = request.get_json()
    output = []
    for tc in data:
        part1 = tc.get("part1")
        part2 = tc.get("part2")
        part3 = tc.get("part3")
        part4 = tc.get("part4")
        
        soln = {
                "part1": sol_p1(part1)
                # "part2": sol_p1(part2),
                # "part3": sol_p1(part3),
                # "part4": sol_p1(part4)
                }
        output.append(soln)

    return jsonify(output)

def sol_p1(part1):
    def amt(y, x):
        if (x == 0 or x == y):
            return fr / pow(2,y) * fringetime(t,y)
        else:
            return amt(y-1, x-1) + amt(y-1, x) - 200

    def fringetime(t, y):
        output = 0
        for i in range(y):
            output += 100 * pow(2*y)/fr
        return t - output

    fr = part1.get("flow_rate")
    t = part1.get("time")
    y = part1.get("row_number")
    x = part1.get("col_number")
    return amt(y, x)


