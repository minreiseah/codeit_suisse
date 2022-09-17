import json
from unittest import result

from flask import request, jsonify
from collections import defaultdict
from myapp import app

@app.route('/calendarDays', methods=['POST'])
def evaluate():
    data = request.get_json()
    inputValue = data.get("numbers")
    result = {"part1": part_one(inputValue), "part2": part_two(inputValue) }
    return result

def part_one():
    
    return result

def part_two():

    return result