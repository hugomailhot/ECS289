# !/usr/bin/env python
# encoding: utf-8

"""
This is an daptation of Prim's algorithm, as found in:
Skiena, Steven. The Algorithm Design Manual, 2nd ed. London: Springer-Verlag, 2008.

To compute MSF with n trees in it, compute MST, then remove from it the n-1
edges with highest weight. By doing so you disconnect the MST into n trees,
minimizing the cost by as much as possible, which gives you a MSF.
"""

import numpy as np
import argparse
import sys
import math


def check_args(args=None):
    desc = 'Finds minimum spanning forest with n trees for adjacency matrix m'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-m', '--matrix',
                        help='adjacency matrix m',
                        required=True)
    parser.add_argument('-n', '--n_trees',
                        help='number of trees in the minimum spanning forest',
                        required=True)

    results = parser.parse_args(args)
    return results


def neighbors(m, v):
    """
    Returns a list of neighbors of vertex v in adjacency matrix m.
    """
    return [x for x in range(len(m)) if m[v][x] != 0]

def get_minimum_edge_cost(m, v):
    """
    Return minimum edge cost for vertex v in adjacency matrix m.
    """
    return min([m[v][nb] for nb in neighbors(m, v)])

def minimum_spanning_forest_prim(m, n):
    """
    Given an adjacency matrix m, will return the MSF with n trees.

    Args:
        m (numpy.ndarray) : adjacency matrix representation of the graph
        n (int) : number of trees wanted in result

    Returns:
        mst (list): List of edges in the MSF
    """
    cost = {x: math.inf for x in range(len(m))}
    parent = {x: None for x in range(len(m))}

    # Vertex 0 will be the root
    cost[0] = 0
    unseen = list(range(len(m)))
    mst = []

    while unseen:
        curr = min(unseen, key=cost.__getitem__)
        unseen.remove(curr)

        if parent[curr] is not None:
            mst.append((curr, parent[curr]))
        for nb in neighbors(m, curr):
            if nb in unseen and m[curr][nb] < cost[nb]:
                parent[nb] = curr
                cost[nb] = m[curr][nb]

    mst = sorted(mst, key=lambda x: m[x[0]][x[1]])
    return mst[:-(n-1)]


if __name__ == '__main__':
    # Get command line arguments
    args = check_args(sys.argv[1:])
    # Load adjacency matrix
    m = np.load(args.matrix)
    n_trees = int(args.n_trees)
    msf = minimum_spanning_forest_prim(m, n_trees)
    cost = sum([m[x][y] for x, y in msf])
    print('MSF with {} trees for {}: {}'.format(n_trees,
                                                args.matrix,
                                                [(x+1, y+1) for x,y in list(msf)]))
    print('cost: {}'.format(cost))