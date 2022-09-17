import logging
import json
import numpy as np

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)


@app.route('/stig/warmup', methods=['POST'])
def warmup():
    data = request.get_json()
    logging.info(data)
    questions = data[0].get("questions")
    lower = int(questions[0][0])
    higher = int(questions[0][1])
    max = int(data[0].get("maxRating"))
    right = 0
    for i in range(1,max+1):
        if lower <= i and i <= higher:
            guess = lower
        elif lower > 1:
            guess = 1
        else:
            guess = higher + 1
        if guess == i:
            right += 1

    gcd = np.gcd(right, max)
    result = {}
    result["p"] = int(right / gcd)
    result["q"] = int(max / gcd)
    return json.dumps(result)
