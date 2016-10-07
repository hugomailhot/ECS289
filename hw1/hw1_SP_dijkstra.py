# !/usr/bin/env python
# encoding: utf-8

"""
This is an implementation of Dijkstra's algorithm, as found on this page:
https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
"""

import numpy as np
import argparse
import sys
import math

def check_args(args=None):
    parser = argparse.ArgumentParser(description='Computes shortest path between nodes i and j in matrix m')
    parser.add_argument('-i', '--source',
                        help='source node i',
                        required=True)
    parser.add_argument('-j', '--destination',
                        help='destination node j',
                        required=True)
    parser.add_argument('-m', '--matrix',
                        help='adjacency matrix m',
                        required=True)

    results = parser.parse_args(args)
    return results

def shortest_path(i, j, m):
    """
    Given an adjacency matrix m, source node i and destination node j,
    will return the shortest path from i to j in m.

    Args:
        i (int) : source node
        j (int) : destination node
        m (numpy.ndarray) : adjacency matrix representation of the graph

    Returns:
        sp (tuple): A 2-tuple containing ([path_nodelist], cost_int)
    """

    # Every node starts with infinite distance from i, except i, which starts with
    # distance 0 from itself.
    temp_dist = {x: math.inf for x in range(len(m))}
    temp_dist[i] = 0

    # Maintain a list of node parents to retrieve path at the end
    prev = [None] * len(m)

    unvisited = set(range(len(m)))

    while j in unvisited:
        # Select unvisited node with min temp_dist as current node (source on first loop)
        curr = min(unvisited, key=temp_dist.__getitem__)

        neighbors = [index for index, dist in enumerate(m[curr])
                     if (dist != 0 and index in unvisited)]
        for nb in neighbors:
            new_dist = temp_dist[curr] + m[curr][nb]
            if new_dist < temp_dist[nb]:
                temp_dist[nb] = new_dist
                prev[nb] = curr

        # Remove current node from unvisited
        unvisited -= set([curr])

    # Retrieve shortest path
    path = []
    curr = j
    path.append(curr)
    while prev[curr] is not None:
        path.append(prev[curr])
        curr = prev[curr]
    # Path needs to be reversed to be in chronological order
    path.reverse()

    # Sum all distance values of edges on path
    total_dist = sum([m[a][b] for a,b in zip(path, path[1:])])
    edges = [(a, b) for a, b in zip(path, path[1:])]

    return {'nodes': path, 'edges': edges, 'cost': total_dist}

if __name__ == '__main__':
    # Get command line arguments
    args = check_args(sys.argv[1:])
    # Matrix is zero-indexed, graph is one-indexed
    i, j = int(args.source)-1, int(args.destination)-1
    # Load adjacency matrix
    m = np.load(args.matrix)


    if i < 0 or j < 0 or i >= len(m) or j >= len(m):
        raise IndexError("Node indices not in matrix range (0, {})".format(len(m)))

    res = shortest_path(i, j, m)
    i, j = i+1, j+1
    nodes = [x+1 for x in res['nodes']]
    print('Shortest path from {} to {} is: {}'.format(i, j, nodes))
    print('Total distance is: {}'.format(res['cost']))
    print('Edges are: {}'.format(list(res['edges'])))
