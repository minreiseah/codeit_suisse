from collections import defaultdict


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
    timestamp_dict = defaultdict(lambda: [])
    cqty_dict = defaultdict(lambda: 0)
    cntl_dict = defaultdict(lambda: 0)
    p_qty_dict = defaultdict(lambda: 0)

    for row in df:
        timestamp = row[0]
        ticker = row[1]
        qty = int(row[2])
        price = float(row[3])

        # update cumulative quantity & notional
        cqty_dict[ticker] += qty
        cntl_dict[ticker] += qty * price

        # cumulative delay adjustment
        d = cqty_dict[ticker] % quantity_block
        bqty = cqty_dict[ticker]
        bntl = cntl_dict[ticker]

        # if current qty is not a multiple of quantity_block,
        # then if adjustment adds value,
        # then update qty and ntl
        if(d):
            bqty = cqty_dict[ticker] - d
            bntl = cntl_dict[ticker] - d * price
            # if adding quantity does not move up >0 qty_block tranches
            # then, do not add to notional
            if(bqty == p_qty_dict[ticker]):
                bqty = 0

        # update quantity of previous ticker
        p_qty_dict[ticker] = bqty

        t_row = [ticker, bqty, round(bntl, 1)]
        timestamp_dict[timestamp].append(t_row)

    # add data into output list
    output = []
    for k, v in timestamp_dict.items():
        buffer = []
        for row in v:
            qty = row[1]
            # only add quantities of multiples quantity_block
            if(qty % quantity_block == 0 and qty):
                buffer.append(','.join(str(x) for x in row))

        # add timestamp after to account for multiple tickers
        if buffer:
            buffer.insert(0, k)
            output.append(','.join(buffer))

    # print("output", output)
    return output


to_cumulative_delayed([
    '00:00,A,6,5.6',
    '00:01,A,5,5.6',
    '00:02,A,1,5.6',
], 5)

to_cumulative_delayed([
    '00:05,A,1,5.6',
    '00:00,A,1,5.6',
    '00:02,A,1,5.6',
    '00:03,A,1,5.6',
    '00:04,A,1,5.6',
    '00:06,A,4,5.6',
], 5)

to_cumulative_delayed([
    # '00:01,A,5,5.5',
    # '00:00,A,4,5.6',
    '00:00,B,5,5.5',
    '00:02,B,4,5.6',
], 5)
