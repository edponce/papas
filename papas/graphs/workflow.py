#!/usr/bin/env python3


__all__ = ['WorkflowGraph']


import utils.logger
import graphviz
import copy
import json


class WorkflowGraph(graphviz.Digraph):

    _workflow_id = 0
    _logger = utils.logger.init_logger('WorkflowGraph')
    _styles = {
        'graph': {
            'label': 'Workflow Graph',
            'fontsize': '16',
            'fontcolor': 'white',
            'bgcolor': '#333333',
            'rankdir': 'TB'
        },
        'nodes': {
            'fontname': 'Helvetica',
            'shape': 'hexagon',
            'fontcolor': 'white',
            'color': 'white',
            'style': 'filled',
            'fillcolor': '#006699'
        },
        'edges': {
            'style': 'dashed',
            'color': 'white',
            'arrowhead': 'open',
            'fontname': 'Courier',
            'fontsize': '12',
            'fontcolor': 'white'
        }
    }

    @property
    def nodes(self):
        return self._nodes

    @nodes.setter
    def nodes(self, nodelist):
        if not isinstance(nodelist, list):
            nodelist = [nodelist]

        for node in nodelist:
            try:
                if isinstance(node, list):
                    node = tuple(node)

                # node with attributes
                if isinstance(node, tuple) and len(node) == 2:
                    if (isinstance(node[0], str) and node[0]) \
                        and isinstance(node[1], dict):
                        if node[0] not in self.nodes:
                            self._nodes.append(node[0])
                            self.node(node[0], **node[1])
                    else:
                        raise ValueError

                # node without attributes
                elif isinstance(node, str) and node:
                    if node not in self.nodes:
                        self._nodes.append(node)
                        self.node(node)
                else:
                    raise ValueError

            except ValueError as err:
                WorkflowGraph._logger.error('{0}: Nodes must be a list of strings, {1}'.format(self.id, err))

    @property
    def edges(self):
        return self._edges

    @edges.setter
    def edges(self, edgelist):
        if not isinstance(edgelist, list):
            edgelist = [edgelist]

        for edge in edgelist:
            try:
                if isinstance(edge, list):
                    edge = tuple(edge)
                elif not isinstance(edge, tuple):
                    raise ValueError

                # edge with attributes
                if isinstance(edge[0], list):
                    edge[0] = tuple(edge[0])
                if (isinstance(edge[0], tuple) and len(edge[0]) == 2) \
                    and isinstance(edge[1], dict):
                    if all([(isinstance(e, str) and e) for e in edge[0]]):
                        if edge[0] not in self.edges:
                            self.nodes = list(edge[0])
                            self._edges.append(edge[0])
                            self.edge(*edge[0], **edge[1])
                    else:
                        raise ValueError

                # edge without attributes
                elif all([(isinstance(e, str) and e) for e in edge]):
                    if edge not in self.edges:
                        self.nodes = list(edge)
                        self._edges.append(edge)
                        self.edge(*edge)
                else:
                    raise ValueError

            except ValueError as err:
                WorkflowGraph._logger.error('{0}: Edges must be a single/list tuple of strings, {1}'.format(self.id, err))

    def __init__(self, **conf):
        WorkflowGraph._workflow_id += 1
        self.id = WorkflowGraph._workflow_id
        self._nodes = []
        self._edges = []

        # graphviz.Digraph does not contain this data members
        self.name = 'workflow'
        self.comment = ''
        self.filename = self.name
        self.directory = ''
        self.format = 'pdf'
        self.engine = 'dot'
        self.encoding = 'utf-8'
        self.graph_attr = {}
        self.node_attr = {}
        self.edge_attr = {}
        self.body = []
        self.strict = False

        # list of nodes
        if '_nodes' in conf:
            if isinstance(conf['_nodes'], list):
                self.nodes = conf['_nodes'][:]
            del conf['_nodes']
        elif 'nodes' in conf:
            if isinstance(conf['nodes'], list):
                self.nodes = conf['nodes'][:]
            del conf['nodes']

        # list of edges
        if '_edges' in conf:
            if isinstance(conf['_edges'], list):
                self.edges = conf['_edges'][:]
            del conf['_edges']
        elif 'edges' in conf:
            if isinstance(conf['edges'], list):
                self.edges = conf['edges'][:]
            del conf['edges']

        # graph name used in the source code
        if 'name' not in conf or not isinstance(conf['name'], str):
            conf['name'] = self.name

        # comment added to the first line of the source
        if 'comment' not in conf or not isinstance(conf['comment'], str):
            conf['comment'] = self.comment

        # filename for saving the source
        if 'filename' not in conf or not isinstance(conf['filename'], str):
            conf['filename'] = self.filename

        # directory for source saving and rendering
        if 'directory' not in conf or not isinstance(conf['directory'], str):
            conf['directory'] = self.directory

        # rendering output format
        if '_format' in conf and conf['_format'] in ['pdf', 'png', 'svg', 'plain']:
            conf['format'] = conf['_format']
            del conf['_format']
        if 'format' not in conf or conf['format'] not in ['pdf', 'png', 'svg', 'plain']:
            conf['format'] = self.format

        # layout command used
        if '_engine' in conf and conf['_engine'] in ['dot', 'neato', 'circo']:
            conf['engine'] = conf['_engine']
            del conf['_engine']
        if 'engine' not in conf or conf['engine'] not in ['dot', 'neato', 'circo']:
            conf['engine'] = self.engine

        # encoding for saving source
        if '_encoding' in conf and conf['_encoding'] in ['utf-8', 'us-ascii']:
            conf['encoding'] = conf['_encoding']
            del conf['_encoding']
        if 'encoding' not in conf or conf['encoding'] not in ['utf-8', 'us-ascii']:
            conf['encoding'] = self.encoding

        # mapping of (attribute, value) pairs for the graph
        if 'graph_attr' not in conf or not isinstance(conf['graph_attr'], dict):
            conf['graph_attr'] = self.graph_attr

        # mapping of (attribute, value) pairs for all nodes
        if 'node_attr' not in conf or not isinstance(conf['node_attr'], dict):
            conf['node_attr'] = self.node_attr

        # mapping of (attribute, value) pairs for all edges
        if 'edge_attr' not in conf or not isinstance(conf['edge_attr'], dict):
            conf['edge_attr'] = self.edge_attr

        # iterable of verbatim lines to add to the graph body
        if 'body' not in conf or not isinstance(conf['body'], list):
            conf['body'] = self.body

        # rendering should merge multi-edges
        if 'strict' not in conf or not isinstance(conf['strict'], bool):
            conf['strict'] = self.strict

        try:
            super().__init__(**conf)

        except Exception as err:
            WorkflowGraph._logger.error('{0}: Failed to initialize workflow, {1}'.format(self.id, err))

    def saves(self):
        try:
            if self.nodes:
                super().save()

        except Exception as err:
            WorkflowGraph._logger.warn('{0}: Failed to save workflow, {1}'.format(self.id, err))

    def renders(self):
        try:
            if self.nodes:
                super().render(view=True)

        except Exception as err:
            WorkflowGraph._logger.warn('{0}: Failed to render workflow, {1}'.format(self.id, err))

    def __repr__(self):
        nodes_str = 'Workflow {0}: {1}\n'.format(self.id, self.filename)
        nodes_str += '\tNodes: {0}\n'.format(str(self.nodes))
        nodes_str += '\tEdges: {0}\n'.format(str(self.edges))

        return nodes_str

    @staticmethod
    def json_load(fn):
        wf = None
        try:
            with open(fn, 'r') as fd:
                wf_dict = json.load(fd)
            wf = WorkflowGraph(**wf_dict)

        except Exception as err:
            WorkflowGraph._logger.error('Failed to load workflow from JSON file ({0}), {1}'.format(fn, err))

        return wf

    def json_save(self, fn=''):
        try:
            wf_dict = {}
            for k,v in self.__dict__.items():
                # Skip ID to prevent collisions
                if k not in ['id']:
                    wf_dict[k] = copy.deepcopy(v)

            if not fn:
                fn = self.name + '.json'

            with open(fn, 'w') as fd:
                wf_dict = json.dump(wf_dict, fd)

        except Exception as err:
            WorkflowGraph._logger.error('{0}: Failed to dump workflow into JSON file ({1}), {2}'.format(self.id, fn, err))

    def style(self, styles={}):
        if styles:
            if 'graph' in styles:
                self.graph_attr.update(styles['graph'])
            if 'nodes' in styles:
                self.node_attr.update(styles['nodes'])
            if 'edges' in styles:
                self.edge_attr.update(styles['edges'])
        else:
            if 'graph' in WorkflowGraph._styles:
                self.graph_attr.update(WorkflowGraph._styles['graph'])
            if 'nodes' in WorkflowGraph._styles:
                self.node_attr.update(WorkflowGraph._styles['nodes'])
            if 'edges' in WorkflowGraph._styles:
                self.edge_attr.update(WorkflowGraph._styles['edges'])
