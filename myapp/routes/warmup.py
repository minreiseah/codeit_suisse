import logging
import json
import numpy as np

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)


@app.route('/stig/warmup', methods=['POST'])
def warmup():
    data = request.get_json()
    # logging.info(data)
    interview = data[0]
    max = interview["maxRating"]
    guessable = 0
    add_one = False
    for rating in range(1,max+1):
        floor = max
        unasked = True
        for pair in interview["questions"]:
            if pair["lower"] <= rating and rating <= pair["upper"] and pair["lower"] < floor:
                floor = pair["lower"]
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
    return json.dumps(result)
