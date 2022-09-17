def make_graph(grid):
    height = len(grid)
    width = len(grid[0])
    # V is the set of all indices
    V = list()
    for i in range(height):
        for j in range(width):
            V.append((i,j))

    # E is the set of all pairs of adjacent vertices
    E = set()
    for vertex in V:
        x = vertex[0]
        y = vertex[1]
        top_vertex = (x, y-1)
        bottom_vertex = (x, y+1)
        right_vertex = (x+1, y)
        left_vertex = (x-1, y)
        if(top_vertex in V):
            E.append(set(vertex, top_vertex))
        if(bottom_vertex in V):
            E.append(set(vertex, bottom_vertex))
        if(right_vertex in V):
            E.append(set(vertex, right_vertex))
        if(left_vertex in V):
            E.append(set(vertex, left_vertex))

    return (V,E)

grid = make_grid(data)
start_idx = get_start(grid)

V = set(1,2,3,4,5)
E = set((1,2), (2,4), (4,5))
graph = (V,E)

def dijkstra(graph, src):



