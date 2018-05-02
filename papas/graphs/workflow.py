#!/usr/bin/env python3


__all__ = ['WorkflowGraph']


import utils.logger
import graphviz
import copy
import json


class WorkflowGraph(graphviz.Digraph):

    _workflow_id = 0

    def __init__(self, **conf):
        self._logger = utils.logger.init_logger(self.__class__.__name__)
        self._id = self._workflow_id + 1
        self._name = 'workflow'  # graph name used in the source code
        self._filename = self._name  # filename for saving the source
        self._format = 'pdf'  # rendering output format
        self._engine = 'dot'  # layout command used
        self.__nodes = []
        self.__edges = []

        if '_name' in conf and isinstance(conf['_name'], str):
            self._name = conf['_name']
        if '_filename' in conf and isinstance(conf['_filename'], str):
            self._filename = conf['_filename']
        if '_format' in conf and conf['_format'] in ['pdf', 'png', 'svg', 'plain']:
            self._format = conf['_format']
        if '_engine' in conf and conf['_engine'] in ['dot', 'neato', 'circo']:
            self._engine = conf['_engine']

        super().__init__(name=self._name, filename=self._filename, format=self._format, engine=self._engine)

        if '__nodes' in conf:
            self._nodes = conf['__nodes']
        if '__edges' in conf:
            self.__edges = conf['__edges']

    @property
    def nodes(self):
        print('getter nodes')
        return self.__nodes

    @nodes.setter
    def nodes(self, nodelist=[]):
        print('setter nodes')
        if not isinstance(nodelist, list):
            nodelist = list(nodelist)

        for node in nodelist:
            try:
                if not isinstance(node, str) or len(node) < 1:
                    raise ValueError
                if node not in self.__nodes:
                    self.__nodes.append(node)
                    self.node(node)
            except ValueError as err:
                self._logger.error('{0}: Nodes must be a list of strings'.format(self._id))

    @nodes.deleter
    def nodes(self):
        self.__nodes = []

    @property
    def edges(self):
        print('getter edges')
        return self.__edges

    @edges.setter
    def edges(self, edgelist=[]):
        print('setter edges')
        if not isinstance(edgelist, list):
            edgelist = list(edgelist)

        for edge in edgelist:
            try:
                if not isinstance(edge, tuple) or len(edge) < 2:
                    raise ValueError
                if edge not in self.__edges:
                    if not all([isinstance(e, str) for e in edge]):
                        raise ValueError
                    self.__nodes = edge[0]
                    self.__nodes = edge[1]
                    self.__edges.append(edge)
                    self.edge(edge[0], edge[1])
            except ValueError as err:
                self._logger.error('{0}: Edges must be a single/list tuple of strings'.format(self._id))

    @edges.deleter
    def edges(self):
        self.__edges = []

    def dump(self):
        if self._nodes:
            super().save(self._filename)

    def render(self):
        try:
            if self._nodes:
                super().render(self._filename)
        except:
            self._logger.warn('{0}: Failed to render workflow')
            pass

    def __repr__(self):
        nodes_str = 'Workflow {0}: {1}\n'.format(self._id, self._filename)
        nodes_str += '\tNodes: {0}\n'.format(str(self.__nodes))
        nodes_str += '\tEdges: {0}\n'.format(str(self.__edges))
        return nodes_str

    @staticmethod
    def json_load(fn):
        wf = None
        try:
            with open(fn, 'r') as fd:
                wf_dict = json.load(fd)
            wf = WorkflowGraph(**wf_dict)
        except:
            print('{0}: Failed to load workflow from JSON file, {0}'.format(fn))
        return wf

    @staticmethod
    def json_dump(wf, fn=''):
        try:
            if not isinstance(wf, WorkflowGraph):
                raise

            wf_dict = {}
            for k,v in wf.__dict__.items():
                # Skip logger object, not serializable
                # Skip ID to prevent collisions
                if k not in ['_logger', '_id']:
                    wf_dict[k] = copy.deepcopy(v)

            if not fn:
                fn = wf_dict['filename'] + '.json'

            with open(fn, 'w') as fd:
                wf_dict = json.dump(wf_dict, fd)
        except:
            print('{0}: Failed to dump workflow into JSON file, {0}'.format(fn))
