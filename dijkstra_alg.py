# coding: utf-8

from collections import defaultdict
from heapq import heappop, heappush
# import sys


# Create graph from file of (vertex, edge, weight)
def from_file(f_name):
    G = defaultdict(set)
    with open(f_name) as f:
        for l in f.readlines()[1:]:
            (v, u, w) = map(int, l.split())
            if w <= 0:
                print 'ERROR! Edge weight is incorrect:', w
                return {}
            if v != u:                        # reject self-directed edges
                G[v].add((w, u))              # reject duplicate edges
    return G


# Search minimal cost from start to goal and path (or multi-path for same cost)
def dij(G, start, goal):
    V = set()                              # set of visited vertex
    V_add = V.add                          # speedup (method address calc once)
    C = defaultdict(lambda: float('inf'))  # dict of cost (inf by default)
    C[start] = 0                           # distance from start to start is 0
    P = defaultdict(list)                  # dict of multi-path (predecessors pointers)
    P[start] = [None]                      # predecessor for start is None
    Q = [(0, start)]                       # min-priority queue of tuple (cost, vertex)

    while Q:
        (cost_v, v) = heappop(Q)
        if v == goal:
            return cost_v, P
        if v not in V:
            V_add(v)
            for (w, u) in G[v]:
                if u not in V:
                    cost_u = cost_v + w
                    if C[u] > cost_u:
                        C[u], P[u] = cost_u, [v]
                        heappush(Q, (cost_u, u))
                    elif C[u] == cost_u:
                        P[u].append(v)
    return None, None


# Example source file:
f_name = 'USA-FLA.txt'  # 1,070,376 vertexes and 2,712,798 edges /50Mb

# Graph created once and can be used repeatedly
G = from_file(f_name)  # ~7sec/48Mb for USA-FLA.txt (24896 duplicated edges rejected!)


# Example start and goal vertexes
(start, goal) = 100562, 1070345

if G:
    if G[start]:
        if G[goal]:
            # search cost and multi-path
            (cost, P) = dij(G, start, goal)  # ~3sec/48Mb for USA-FLA.txt # print sys.getsizeof(P)//1048576, 'MB'
            if cost:
                print 'Cost:', cost, '( from', start, 'to', goal, ')'
                # todo: reverse_path from P
            else:
                print 'No path from start to goal!'
        else:
            print 'Error: goal vertex not exist!'
    else:
        print 'Error: start vertex not exist!'
else:
    print 'Error: graph is empty!'
