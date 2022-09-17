import logging
import json

from flask import request, jsonify

import numpy as np

from myapp import app

@app.route('/rubiks', methods=['POST'])
def rubiks():
    data = request.get_json()
    ops = data.get("ops")
    state = data.get("state")

    cube = Cube(state)
    ops = process_ops(ops)

    for op in process_ops(ops):
        cube.step(op)

    result = cube.get_cube()

    return result

class Cube:
    def __init__(self, state):
        self.up = np.array(state["u"])
        self.left = np.array(state["l"])
        self.front = np.array(state["f"])
        self.right = np.array(state["r"])
        self.back = np.array(state["b"])
        self.down = np.array(state["d"])


    def get_cube(self):
        out = {
            "u": self.up.tolist(),
            "l": self.left.tolist(),
            "f": self.front.tolist(),
            "r": self.right.tolist(),
            "b": self.back.tolist(),
            "d": self.down.tolist()
            }
        return out

    def rotate_up(self, clockwise = True):
        if(clockwise):
            self.up = rotate_clockwise(self.up)
            tmp = self.front[0,:].copy()
            self.front[0,:] = self.right[0,:]
            self.right[0,:] = self.back[0,:]
            self.back[0,:] = self.left[0,:]
            self.left[0,:] = tmp
        else:
            self.up = rotate_anticlockwise(self.up)
            tmp = self.front[0,:].copy()
            self.front[0,:] = self.left[0,:]
            self.left[0,:] = self.back[0,:]
            self.back[0,:] = self.right[0,:]
            self.right[0,:] = tmp

    def rotate_down(self, clockwise = True):
        if(clockwise):
            self.down = rotate_clockwise(self.down)
            tmp = self.front[2,:].copy()
            self.front[2,:] = self.left[2,:]
            self.left[2,:] = self.back[2,:]
            self.back[2,:] = self.right[2,:]
            self.right[2,:] = tmp
        else:
            self.down = rotate_anticlockwise(self.down)
            tmp = self.front[2,:].copy()
            self.front[2,:] = self.right[2,:]
            self.right[2,:] = self.back[2,:]
            self.back[2,:] = self.left[2,:]
            self.left[2,:] = tmp

    def rotate_left(self, clockwise = True):
        if(clockwise):
            self.left = rotate_clockwise(self.left)
            tmp = self.up[:,0].copy()
            self.up[:, 0] = np.flip(self.back[:, 2])
            self.back[:, 2] = np.flip(self.down[:,0])
            self.down[:, 0] = self.front[:, 0]
            self.front[:, 0] = tmp
        else:
            self.left = rotate_anticlockwise(self.left)
            tmp = self.up[:, 0].copy()
            self.up[:, 0] = self.front[:, 0]
            self.front[:, 0] = self.down[:, 0]
            self.down[:, 0] = np.flip(self.back[:, 2])
            self.back[:, 2] = np.flip(tmp)

    def rotate_right(self, clockwise = True):
        if(clockwise):
            self.right = rotate_clockwise(self.right)
            tmp = self.up[:, 2].copy()
            self.up[:, 2] = np.flip(self.front[:, 2])
            self.front[:, 2] = self.down[:, 2]
            self.down[:, 2] = np.flip(self.back[:, 0])
            self.back[:, 0] = tmp
        else:
            self.right = rotate_anticlockwise(self.right)
            tmp = self.up[:,2].copy()
            self.up[:, 2] = np.flip(self.back[:, 0])
            self.back[:, 0] = np.flip(self.down[:,2])
            self.down[:, 2] = self.front[:, 2]
            self.front[:, 2] = tmp


    def rotate_front(self, clockwise = True):
        if(clockwise):
            self.front = rotate_clockwise(self.front)
            tmp = self.up[2, :].copy()
            self.up[2, :] = np.flip(self.left[:, 2])
            self.left[:, 2] = self.down[0, :]
            self.down[0, :] = np.flip(self.right[:, 0])
            self.right[:, 0] = tmp
        else:
            self.front = rotate_anticlockwise(self.front)
            tmp = self.up[2, :].copy()
            self.up[2, :] = np.flip(self.right[:, 0])
            self.right[:, 0] = self.down[0, :]
            self.down[0, :] = np.flip(self.left[:, 2])
            self.left[:, 2] = tmp

    def rotate_back(self, clockwise = True):
        if(clockwise):
            self.back = rotate_clockwise(self.back)
            tmp = self.up[0, :].copy()
            self.up[0, :] = np.flip(self.right[:, 2])
            self.right[:, 2] = self.down[2, :]
            self.down[2, :] = np.flip(self.left[:, 0])
            self.left[:, 0] = tmp
        else:
            self.back = rotate_anticlockwise(self.back)
            tmp = self.up[0, :].copy()
            self.up[0, :] = np.flip(self.left[:, 0])
            self.left[:, 0] = self.down[2, :]
            self.down[2, :] = np.flip(self.right[:, 2])
            self.right[:, 2] = tmp
    
    def step(self, op):
        is_clockwise = len(op) == 1
        s = op[0]
        if s == 'U':
            self.rotate_up(is_clockwise)
        elif s == 'L':
            self.rotate_left(is_clockwise) 
        elif s == 'F':
            self.rotate_front(is_clockwise)
        elif s == 'R':
            self.rotate_right(is_clockwise)
        elif s == 'B':
            self.rotate_back(is_clockwise)
        else:
            self.rotate_down(is_clockwise)


# helper functions

def rotate_clockwise(side):
    return np.rot90(side, 3)

def rotate_anticlockwise(side):
    return np.rot90(side)

def process_ops(s):
    res = []
    counter = 0
    length = len(s)
    while(counter < length):
        if(length - counter == 1):
            res.append(s[counter])
            break
        elif(s[counter + 1] == 'i'):
            res.append(s[counter : counter+2])
            counter += 2
        else:
            res.append(s[counter])
            counter += 1
    return res


# cube = Cube(state)
#
# for op in process_ops("UiD"):
#     step(op)
#
# output = cube.get_cube()
#
# for k in output:
#     print(k)
#     for v in output[k]:
#         print(v)

# "u": [["w", "w", "w"], ["w", "w", "w"], ["w", "w", "w"]],
# "l": [["p", "p", "p"], ["p", "p", "p"], ["p", "p", "p"]],
# "f": [["b", "b", "b"], ["b", "b", "b"], ["b", "b", "b"]],
# "r": [["o", "o", "o"], ["o", "o", "o"], ["o", "o", "o"]],
# "b": [["g", "g", "g"], ["g", "g", "g"], ["g", "g", "g"]],
# "d": [["y", "y", "y"], ["y", "y", "y"], ["y", "y", "y"]]
