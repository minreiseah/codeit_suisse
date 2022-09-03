def to_cumulative_delayed(stream: list, quantity_block: int):
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
    # hqty_dict = {}
    # hntl_dict = {}
    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])
        prev_qty = 0
        prev_price = 0
        if(ticker in cqty_dict):
            prev_qty = cqty_dict[ticker]
            prev_price = cntl_dict[ticker]
            cqty_dict[ticker] += qty
            cntl_dict[ticker] += qty * price
        else:
            cqty_dict[ticker] = qty
            cntl_dict[ticker] = qty * price

        # cumulative delay adjustment
        d = cqty_dict[ticker] % quantity_block
        bqty = cqty_dict[ticker]
        bntl = cntl_dict[ticker]
        if(d):
            bqty = cqty_dict[ticker] - d
            bntl = cntl_dict[ticker] - d * price
            # remove duplicates
            if(bqty == prev_qty and bntl == prev_price):
                bqty = 0
                bntl = 0

        t_row = [ticker, bqty, bntl]
        if(timestamp in timestamp_dict):
            timestamp_dict[timestamp].append(t_row)
        else:
            timestamp_dict[timestamp] = [t_row]

    # add data into output list
    output = []
    for k, v in timestamp_dict.items():
        buffer = []
        for row in v:
            qty = row[1]
            if(qty % quantity_block == 0 and qty):
                buffer.append(','.join(str(x) for x in row))
        if buffer:
            buffer.insert(0, k)
            output.append(','.join(buffer))

    print("output", output)
    return output


to_cumulative_delayed([
    '00:05,A,1,5.6',
    '00:00,A,1,5.6',
    '00:02,A,1,5.6',
    '00:03,A,1,5.6',
    '00:04,A,1,5.6',
    '00:06,A,4,5.6',
], 5)

to_cumulative_delayed([
    '00:01,A,5,5.5',
    '00:00,A,4,5.6',
    '00:00,B,5,5.5',
    '00:02,B,4,5.6',
], 5)
