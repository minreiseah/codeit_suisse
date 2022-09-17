import json

from flask import request, jsonify
from collections import defaultdict
from myapp import app

@app.route('/tickerStreamPart1', methods=['POST'])
def tickerstreampart1():
    data = request.get_json()
    stream = data.get("stream")
    result = {"output": to_cumulative(stream)}
    return json.dumps(result)

def to_cumulative(stream: list):

    # create 2d list for stream
    df = []
    for row in stream:
        row = row.split(',')
        df.append(row)

    # sort df by timestamp
    df.sort(key= lambda i: i[0])

    # list stores the aggregated stream
    new_df = [[df[0][0]]]

    # dicts keep track of cumulative quantity and notional for each ticker
    c_qty = defaultdict(lambda: 0)
    c_not = defaultdict(lambda: 0)
    
    # set keeps track of tickers that appear at current timestamp
    tickers_here = set()

    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        
        # if timestamp is different from previous timestamp
        if timestamp != new_df[-1][0]:
            # append [ticker, c_qty, c_not] for each element in tickers_here, and clear it once done
            for tickers in sorted(tickers_here):
                new_df[-1].extend([tickers, c_qty[tickers], round(c_not[tickers],1)])
            tickers_here.clear()
            # add a new row
            new_df.append([timestamp])
        
        # update cumulatives
        c_qty[ticker] += qty
        c_not[ticker] += qty * price

        # remember ticker at this timestamp
        tickers_here.add(ticker)

    # add last row
    for tickers in sorted(tickers_here):
        new_df[-1].extend([tickers, c_qty[tickers], round(c_not[tickers],1)])

    # flatten new_df using list comprehension magic
    output = []
    for row in new_df:
        output.append(",".join([str(i) for i in row]))

    return output

@app.route('/tickerStreamPart2', methods=['POST'])
def tickerstreampart2():
    data = request.get_json()
    stream = data.get("stream")
    quantity_block = data.get("quantityBlock")
    result = {"output" : to_cumulative_delayed(stream, quantity_block)}
    return result

def to_cumulative_delayed(stream: list, quantity_block: int):

    # create 2d list for stream
    df = []
    for row in stream:
        row = row.split(',')
        df.append(row)

    # sort df by timestamp
    df = sorted(df, key = lambda x: (x[0], x[1]))

    # list stores the aggregated stream
    new_df = []

    # dicts keep track of cumulative quantity and notional for each ticker
    c_qty = defaultdict(lambda: 0)
    c_not = defaultdict(lambda: 0)

    # dict keeps track of at what quantity each ticker next fills a block
    c_qty_pop = defaultdict(lambda: quantity_block)

    # bool to create the first row wherever the first block is filled
    first_pop = True

    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        
        # update cumulatives
        c_qty[ticker] += qty
        c_not[ticker] += qty * price

        # while quantity_block is filled
        while c_qty[ticker] >= c_qty_pop[ticker]:
            # evaluate and exclude any overflow notional
            overflow = c_qty[ticker] - c_qty_pop[ticker]
            buffer_not = overflow * price
            block_not = c_not[ticker] - buffer_not # this is valid because all overflow tickers should be the price given in current tick
            # append new row to new_df
            if first_pop:
                new_df.append([timestamp, ticker, c_qty_pop[ticker], round(block_not,1)])
                first_pop = False
            elif timestamp == new_df[-1][0]:
                if ticker == new_df[-1][-3]:
                    new_df[-1][-2] = c_qty_pop[ticker]
                    new_df[-1][-1] = round(block_not,1)
                else:
                    new_df[-1].extend([ticker, c_qty_pop[ticker], round(block_not,1)])
            else:
                new_df.append([timestamp, ticker, c_qty_pop[ticker], round(block_not,1)])
            # increment c_qty_pop
            c_qty_pop[ticker] += quantity_block

    # flatten new_df using list comprehension magic
    output = []
    for row in new_df:
        output.append(",".join([str(i) for i in row]))

    return output