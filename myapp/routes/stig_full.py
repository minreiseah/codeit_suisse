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
    interview = data[0]
    maxRating = interview["maxRating"]
    lucky = interview["lucky"]
    p = 1
    decrypted = []
    for pair in interview["questions"]:
        interval = [(pair["upper"] + p*lucky - 1) % maxRating + 1, (pair["lower"] + p*lucky - 1) % maxRating + 1]
        decrypted.append({"lower": min(interval), "upper": max(interval)})
        # logging.info(decrypted)
        guessable = stig_checkhere(maxRating, decrypted)
        gcd = np.gcd(guessable, maxRating)
        p = int(guessable / gcd)
    q = int(maxRating / gcd)
    output.append({"p": p, "q": q})
    return jsonify(output)

def stig_checkhere(maxRating, questions):
    guessable = []
    for rating in range(1,maxRating+1):
        fingerprint = []
        for pair in questions:
            if pair["lower"] <= rating and rating <= pair["upper"]:
                fingerprint.append(1)
            else:
                fingerprint.append(0)
        if fingerprint not in guessable:
            guessable.append(fingerprint)
    return len(guessable)

