import logging
import json
import numpy as np

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)


@app.route('/stig/warmup', methods=['POST'])
def warmup():
    data = request.get_json()
    interview = data[0]
    max = interview["maxRating"]
    lower = np.empty()
    upper = np.empty()
    for pair in interview["questions"]:
        lower = np.append(lower, pair["lower"])
        upper = np.append(upper, pair["upper"])
    guessable = 0
    for rating in range(1,max+1):
        floor = max
        unasked = True
        for pair in range(lower.size):
            if lower[pair] <= rating and rating <= upper[pair] and lower[pair] < floor:
                floor = lower[pair]
                unasked = False
        if rating == floor:
            guessable += 1
        if unasked == True:
            add_one = True
    if add_one == True:
        guessable += 1
    gcd = np.gcd(guessable, max)
    result = {}
    result["p"] = int(guessable / gcd)
    result["q"] = int(max / gcd)
    return [json.dumps(result)]
