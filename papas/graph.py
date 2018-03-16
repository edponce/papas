#!/usr/bin/env python3

import networkx as nx
import json
from networkx.readwrite import json_graph
import re


# Tree operations
# https://networkx.github.io/documentation/stable/_modules/networkx/algorithms/tree/operations.html


gstr = '''
A::Requires = ""
B::Requires = A
C::Requires = B
D::Requires = C
H::Requires = A
'''


def load_digraph(fn=''):
    raw = ''
    with open(fn, 'r') as fd:
        raw = fd.read()
    return raw


def construct_digraph(gstr=''):
    '''
    Constructs a networkx tree graph with a single root
    '''
    regex = re.compile(r'^([A-Z]+)::Requires\s+=\s([A-Z"]+)$')
    G = nx.DiGraph()
    root = None
    for l in gstr.splitlines():
        if len(l):
            target, prereq = regex.match(l).groups()
            if prereq == '""':
                root = target
            else:
                G.add_edge(prereq, target)
    return G, root


def print_digraph(G=None, roots=[]):
    '''
    Prints networkx graph, supports multiple roots
    '''
    for s in roots:
        print(s)
        spacer = {s: 0}
        for prereq, target in nx.dfs_edges(G, s):
            spacer[target] = spacer[prereq] + 2
            print('{spacer}+-{t}'.format(spacer=' ' * spacer[prereq], t=target))


def json_digraph(G=None, root=None):
    '''
    Convert networkx graph into JSON format
    '''
    data = json_graph.tree_data(G, root)
    return data


#gstr = load_digraph('graph.txt')
G, r = construct_digraph(gstr)
print_digraph(G, r)

data = json_digraph(G, r)
s = json.dumps(data)
print(s)
