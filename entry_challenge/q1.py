def to_cumulative(stream: list):
    df = []

    # creation of '2d' array
    for row in stream:
        row = row.split(',')
        df.append(row)

    # sort by time, and ticker
    # implemented in reverse order
    df.sort(key=lambda x: x[1])
    df.sort(key=lambda x: x[0])

    # put data into dicts to track their values over time
    timestamp_dict = {}
    cqty_dict = {}
    cntl_dict = {}
    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        if(ticker in cqty_dict):
            cqty_dict[ticker] += qty
            cntl_dict[ticker] += qty * price
        else:
            cqty_dict[ticker] = qty
            cntl_dict[ticker] = qty * price

        t_row = [ticker, str(cqty_dict[ticker]), str(cntl_dict[ticker])]
        if(timestamp in timestamp_dict):
            timestamp_dict[timestamp] += ',' + ','.join(t_row)
        else:
            timestamp_dict[timestamp] = ','.join(t_row)

    # add data into output list
    output = []
    for k, v in timestamp_dict.items():
        output.append(','.join([k, v]))

    # print(output)
    return output
