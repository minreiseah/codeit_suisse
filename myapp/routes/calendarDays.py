import json
from unittest import result

from flask import request, jsonify
import datetime as dt
from myapp import app

@app.route('/calendarDays', methods=['POST'])
def calendarDays():
    data = request.get_json()
    inputValue = data.get("numbers")
    part1 = part_one(inputValue)
    result = {"part1": part1, "part2": part_two(part1) }
    return result

def part_one(input):
    year = input[0]
    dt_dates = []
    result = []
    if year % 4 == 0:
        year_days = 366
    else:
        year_days = 365
    
    for date in input[1:]:
        if date in range(1,year_days+1):
            dt_date = dt.date(year, 1, 1) + dt.timedelta(date - 1)
            dt_dates.append(dt_date)
    for month in range(1,13):
        thismonth = set()
        for x in filter(lambda y: y.month==month, dt_dates):
            thismonth.add(x.weekday())
        if thismonth == {0,1,2,3,4,5,6}:
            output = "alldays"
        elif thismonth == {0,1,2,3,4}:
            output = "weekday"
        elif thismonth == {5,6}:
            output = "weekend"
        else:
            daynames="mtwtfss"
            output="       "
            for day in thismonth:
                output = output[:day] + daynames[day] + output[day+1:]
        result.append(output)
        string = ",".join(result)+","

    return string

def part_two(input):
    newyear = 2001 + input.find(" ")
    result = [newyear]
    for month in range(1,13):
        indicator = input[(month-1)*8+5]
        first = dt.date(newyear, month, 1)
        while first.weekday() != 0:
            first += dt.timedelta(1)
        if indicator == "y":
            for x in range(7):
                result.append((first.timetuple().tm_yday)+x)
        elif indicator == "a":
            for x in range(5):
                result.append((first.timetuple().tm_yday)+x)
        elif indicator == "n":
            for x in range(5,7):
                result.append((first.timetuple().tm_yday)+x)
        else:
            counter = 0
            for bool in input[(month-1)*8:month*8]:
                if bool != " ":
                    result.append((first.timetuple().tm_yday)+counter)
                counter += 1


    return result