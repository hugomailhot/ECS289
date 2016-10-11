# !/usr/bin/env python
# encoding: utf-8

"""
This is an implementation of Kruskal's algorithm, as found in:
Skiena, Steven. The Algorithm Design Manual, 2nd ed. London: Springer-Verlag, 2008.

--------------------------------------------
Kruskal's algorithm:

Sort the edges in order of increasing weight
count <- 0
while (count < n-1) do
    get next edge (v,w)
    if (component(v) != component(w))
        add (v,w) to MST
        component(v) = component(w)
--------------------------------------------

Credits for UnionFind in unionfind.py
"""

import numpy as np
import argparse
import sys
from unionfind import UnionFind


def check_args(args=None):
    parser = argparse.ArgumentParser(description='Finds minimum spanning tree for adjacency matrix m')
    parser.add_argument('-m', '--matrix',
                        help='adjacency matrix m',
                        required=True)

    results = parser.parse_args(args)
    return results

def minimum_spanning_tree_kruskal(m):
    """
    Given an adjacency matrix m, will return the MST.

    Args:
        m (numpy.ndarray) : adjacency matrix representation of the graph

    Returns:
        mst (list): List of edges in the MST
    """

    # Maintain a UnionFind with component for each node
    # Each node starts in a component of its own, 
    # added when component is first queried for it.
    component = UnionFind()

    # Get all non-zero edges from m's lower triangle,
    # then sort by order of increasing weight.
    edges = [(x,y) for x in range(len(m)) for y in range(x) if m[x][y] != 0]
    edges = sorted(edges, key=lambda x: m[x[0]][x[1]])

    mst = []
    for e in edges:
        if component[e[0]] != component[e[1]]:
            mst.append(e)
            component.union(e[0], e[1])
        if len(mst) >= len(m)-1:
            break

    return mst

if __name__ == '__main__':
    # Get command line arguments
    args = check_args(sys.argv[1:])
    # Load adjacency matrix
    m = np.load(args.matrix)
    mst = minimum_spanning_tree_kruskal(m)
    cost = sum([m[x][y] for x, y in mst])
    print('MST edges for matrix m: {}'.format([(x+1, y+1) for x,y in list(mst)]))
    print('cost: {}'.format(cost))