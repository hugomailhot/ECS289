# !/usr/bin/env python
# encoding: utf-8

"""
This is an implementation of Prim's algorithm, as found in:
Skiena, Steven. The Algorithm Design Manual, 2nd ed. London: Springer-Verlag, 2008.

--------------------------------------------
Prim's algorithm:

Select an arbitrary vertex to start
while (there are fringe vertices)
    select minimum-weight edge between tree and fringe
    add the selected edge and vertex to the tree
    update the cost to all affected fringe vertices
--------------------------------------------
"""

import numpy as np
import argparse
import sys
import math


def check_args(args=None):
    parser = argparse.ArgumentParser(description='Finds minimum spanning tree for adjacency matrix m')
    parser.add_argument('-m', '--matrix',
                        help='adjacency matrix m',
                        required=True)

    results = parser.parse_args(args)
    return results


def neighbors(node, m):
    """
    Returns a list of neighbors of node in m.
    """
    return [x for x in range(len(m)) if m[node][x] != 0]


def minimum_spanning_tree_prim(m):
    """
    Given an adjacency matrix m, will return the MST.

    Args:
        m (numpy.ndarray) : adjacency matrix representation of the graph

    Returns:
        mst (list): List of edges in the MST
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
        for nb in neighbors(curr, m):
            if nb in unseen and m[curr][nb] < cost[nb]:
                parent[nb] = curr
                cost[nb] = m[curr][nb]

    return mst


if __name__ == '__main__':
    # Get command line arguments
    args = check_args(sys.argv[1:])
    # Load adjacency matrix
    m = np.load(args.matrix)
    mst = minimum_spanning_tree_prim(m)
    print('MST edges for matrix m: {}'.format([(x+1, y+1) for x,y in list(mst)]))
