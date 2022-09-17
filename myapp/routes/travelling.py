import logging
import json

from flask import request, jsonify

from myapp import app

logger = logging.getLogger(__name__)

@app.route('/travelling-suisse-robot', methods=['POST'])
def travelling():
    data = request.get_data()
    logging.info(data)
    return data

