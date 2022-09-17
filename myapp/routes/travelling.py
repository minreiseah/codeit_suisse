import logging
import json

from flask import request, jsonify

# from myapp import app

logger = logging.getLogger(__name__)

# @app.route('/travelling-suisse-robot', methods=['POST'])
# def travelling():
#     data = request.get_data()
#     logging.info(dataevaluate)
#     return data



data = b'I\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00O\x00\x00\x00\x00T\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00\x00\x00D\x00\x00\x00X\x00\n\x00E\x00\x00\x00\x00\x00\x00I\x00\n\x00\x00\x00\x00\x00\x00\x00\x00EC\n\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\n\x00\x00U\x00S\x00\x00\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x00\x00S\nS\x00\x00\x00\x00\x00\x00\x00\x00\x00\n'

def make_grid(data):
    str = data.decode()[:-1].split('\n')
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

def get_start(grid):
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if row[j] == 'X':
                return (i, j)

def make_graph(grid):
    height = len(grid)
    width = len(grid[0])
    # V is the set of all indices
    V = list()
    for i in range(height):
        for j in range(width):
            V.append((i,j))

    # E is the set of all pairs of adjacent vertices
    E = list()
    for vertex in V:
        x = vertex[0]
        y = vertex[1]
        right_vertex = (x+1,y)
        left_vertex = (x,y+1)
        if(right_vertex in V):
            E.append((vertex, right_vertex))
        if(left_vertex in V):
            E.append((vertex, left_vertex))

    return (V,E)

grid = make_grid(data)
start_idx = get_start(grid)
graph = make_graph(grid)


