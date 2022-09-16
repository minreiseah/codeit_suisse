import logging
import json

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)


@app.route('/square', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("Data sent for evaluation {}".format(data))
    inputValue = data.get("input")
    result = inputValue * inputValue
    logging.info("My result : {}".format(result))
    return json.dumps(result)
