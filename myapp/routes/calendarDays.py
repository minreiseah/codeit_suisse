import json
from unittest import result

from flask import request, jsonify
import datetime as dt
from myapp import app

@app.route('/calendarDays', methods=['POST'])
def evaluate():
    data = request.get_json()
    inputValue = data.get("numbers")
    result = {"part1": part_one(inputValue), "part2": part_two(inputValue) }
    return result

def part_one(input):
    year = input[0]
    dt_dates = []
    for date in input[1:]:
        dt_date = dt.date(year, 1, 1) + dt.timedelta(date - 1)
        dt_dates.append(dt_date)
    for months in range(1,13):
        thismonth = set()
        for x in filter(lambda y: y.month==months, dt_dates):
            thismonth.add(x.weekday())
        if thismonth == {0,1,2,3,4,5,6}:
            output = "alldays"
        if thismonth == {0,1,2,3,4}:
            output = "weekday"
        if thismonth == {5,6}:
            output = "weekend"
        else:
            daynames="mtwtfss"
            output="       "
            for day in thismonth:
                output[day] = daynames[day]
        result.append(output)
        
    return result

def part_two(input):
    result = "todo"
    return result