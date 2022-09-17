import logging
import json

from flask import request, jsonify
from collections import defaultdict

from myapp import app

logger = logging.getLogger(__name__)

@app.route('/travelling-suisse-robot', methods=['POST'])
def travelling():
    data = request.get_data()
    # logging.info("data given: {}".format(data))
    grid = make_grid(data)
    # logging.info("grid: {}".format(grid))
    indices = get_indices(grid)
    routes = get_routes(indices)

    # get best path
    mn = routes[0]['d']
    mn_idx = 0
    for i in range(len(routes)):
        d = routes[i]['d']
        if(d < mn):
            mn = d
            mn_idx = i

    best_path = routes[mn_idx]['path']
    logging.info("length: {}". format(len(best_path)))
    logging.info("path: {}".format(best_path))
    logging.info("indices: {}".format(indices))

    return best_path



# data = b'I\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00O\x00\x00\x00\x00T\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x00D\x00\x00\x00X\x00\n\x00E\x00\x00\x00\x00\x00\x00I\x00\n\x00\x00\x00\x00\x00\x00\x00\x00EC\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00U\x00S\x00\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00S\nS\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'

# data = '\n\nIEXD\x00\x00CTUSIEOSS\n'


# def make_grid(data):
#     suss = [x for x in data.split('\n') if x != '']
#     output = []
#     for s in suss:
#         output.append(s.replace('\x00', '0'))
#     return output

def make_grid(data):
    str = data.decode()[:-1].split()
    output = []
    for s in str:
        buf = []
        for i in range(len(s)):
            if(s[i] == '\x00'):
                buf += '0'
            else:
                buf += s[i]
        output.append(buf)
    return output

def get_indices(grid):
    indices = defaultdict(lambda: [])
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if row[j] != '0':
                indices[row[j]].append((i,j))
    return dict(indices)


def get_routes(indices):
    def update_route(original_route, traversals):
        r = original_route.copy()
        for traversal in traversals:
            r['path'] += traversal['path']
            r['d'] += traversal['d']
            r['pos'] = traversal['pos']
        return r
    
    # setup
    c = get_distance(indices['X'][0], indices['C'][0], 0)
    route = {'path': c['path'], 'd': c['d'], 'pos': c['pos']}
    o = get_distance(indices['C'][0], indices['O'][0], c['pos'])
    d = get_distance(indices['O'][0], indices['D'][0], o['pos'])
    route = update_route(route, [o,d])

    routes = []

    for e_idx in range(2):
        for i_idx in range(2):
            for s_idx in range(3):
                for s_idx_a in range(2):
                    e0 = get_distance(indices['D'][0], indices['E'][e_idx], d['pos'])
                    i0 = get_distance(indices['E'][e_idx], indices['I'][i_idx], e0['pos'])
                    t = get_distance(indices['I'][i_idx], indices['T'][0], i0['pos'])
                    s0 = get_distance(indices['T'][0], indices['S'][s_idx], t['pos'])
                    u = get_distance(indices['S'][s_idx], indices['U'][0], s0['pos'])
                    i1 = get_distance(indices['U'][0], indices['I'][(i_idx + 1) % 2], u['pos'])

                    s_idx_1 = (s_idx + 1) % 3 if s_idx_a == 0 else (s_idx + 2) % 3
                    s_idx_2 = (s_idx + 2) % 3 if s_idx_a == 0 else (s_idx + 1) % 3

                    s1 = get_distance(indices['I'][0], indices['S'][s_idx_1], i1['pos'])
                    s2 = get_distance(indices['S'][s_idx_1], indices['S'][s_idx_2], s1['pos'])
                    e1 = get_distance(indices['S'][s_idx_2], indices['E'][(e_idx + 1) % 2], s2['pos'])
                routes.append(update_route(route, [e0, i0, t, s0, u, i1, s1, s2, e1]))

    return routes

# change this to return both distance and string path
def get_distance(v1, v2, pos):
    def get_new_pos(pos_diff):
        out = ''
        if pos_diff < 0:
            return -pos_diff * 'L'
        else:
            return pos_diff * 'R'

    str = ''
    y_dist = v2[0] - v1[0]
    x_dist = v2[1] - v1[1]

    if(y_dist < 0): # up
        str += get_new_pos(0 - pos)
        str += -y_dist * 'S'
        pos = 0
    elif(y_dist > 0): # down
        str += get_new_pos(2 - pos)
        str += y_dist * 'S'
        pos = 2

    if(x_dist > 0): # right
        str += get_new_pos(1 - pos)
        str += x_dist * 'S'
        pos = 1
    elif(x_dist < 0): # left
        str += get_new_pos(-1 - pos)
        str += -x_dist * 'S'
        pos = -1

    str += 'P'

    return {'d': abs(y_dist) + abs(x_dist), 
            'pos': pos,
            'path': str}



# # logging.info(data)
# grid = make_grid(data)
# print(grid)
# indices = get_indices(grid)
# routes = get_routes(indices)
#
# # get best path
# mn = 1e9
# mn_idx = 0
# for i in range(len(routes)):
#     d = routes[i]['d']
#     if(d < mn):
#         mn = d
#         mn_idx = i
#
# best_path = routes[mn_idx]['path']
#
# print(grid)
# print(mn)
