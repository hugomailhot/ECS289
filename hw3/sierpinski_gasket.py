# !/usr/bin/env python
# encoding: utf-8

"""
Create a Sierpinki's Gasket using networkx. This script relies on properly
relabeling copies of the top triangle, then using networkx's compose method,
which will merge together two nodes from different graphs if their labels are the same.
"""

import networkx as nx

# For each recursion:
# - Make a l_copy and r_copy of the top_graph
# - Relabel top node from l_copy to match left_node from top_graph
# - Relabel top node from r_copy to match right_node from top_graph
# - Relabel right_node from l_copy and left_node from r_copy to be the same
# - Relabel all other nodes so they are unique
# - Use nx.compose() to merge all three graphs
# - Also return indices for top, leftmost, and rightmost nodes

def sierpinski_step(n):
    """
    n is the number of steps.
    """
    if n == 0:
        # Base case
        return (nx.Graph([(1,2), (2,3), (3,1)]), {'top': 1, 'left': 2, 'right': 3})
    else:
        # Recursion
        top_graph, top_corners = sierpinski_step(n-1)

        # ---------------------------------------------
        # -- Beginning of ugly index management part --
        # ---------------------------------------------
        l_first_idx = max(top_graph.nodes()) + 1
        l_last_idx = l_first_idx + len(top_graph)
        l_label_map = dict(zip(top_graph.nodes(), range(l_first_idx, l_last_idx+1)))
        # Left graph relabels its top corner to top graph's left corner
        l_label_map[top_corners['top']] = top_corners['left']  

        r_first_idx = l_last_idx + 1
        r_last_idx = r_first_idx + len(top_graph)
        r_label_map = dict(zip(top_graph.nodes(), range(r_first_idx, r_last_idx+1)))
        # Right graph relabels its top corner to top graph's right corner
        r_label_map[top_corners['top']] = top_corners['right']
        # Right graph relabels its left corner to left graph's right corner
        r_label_map[top_corners['left']] = l_label_map[top_corners['right']]
        # ---------------------------------------------
        # ----- End of ugly index management part -----
        # ---------------------------------------------

        left_graph = nx.relabel_nodes(top_graph, l_label_map)
        right_graph = nx.relabel_nodes(top_graph, r_label_map)

        composed_graph = nx.compose(top_graph, left_graph)
        composed_graph = nx.compose(composed_graph, right_graph)

    return (composed_graph, {'top': top_corners['top'],
                             'left': l_label_map[top_corners['left']],
                             'right': r_label_map[top_corners['right']]})
