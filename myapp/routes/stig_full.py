import logging
import json
import numpy as np

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)


@app.route('/stig/full', methods=['POST'])
def stig_full():
    data = request.get_json()
    # logging.info(data)
    output = []
    for interview in data:
        max = interview["maxRating"]
        lucky = interview["lucky"]
        guessable = []
        for rating in range(1,max+1):
            fingerprint = []
            for pair in interview["questions"]:
                if pair["lower"] <= rating and rating <= pair["upper"]:
                    fingerprint.append(1)
                else:
                    fingerprint.append(0)
            if fingerprint not in guessable:
                guessable.append(fingerprint)
        gcd = np.gcd(len(guessable), max)
        result = {}
        result["p"] = int(len(guessable) / gcd)
        result["q"] = int(max / gcd)
        output.append(result)
    return json.dumps(output)