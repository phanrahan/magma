from abc import ABC, abstractmethod
from ..is_definition import isdefinition
from .tsort import tsort

__all__ = ['Pass', 'InstancePass', 'DefinitionPass', 'InstanceGraphPass']


class Pass(ABC):
    """Abstract base class for all passes"""
    def __init__(self, main):
        self.main = main

    def run(self):
        self.done()
        return self

    def done(self):
        pass


class InstancePass(Pass):
    def __init__(self, main):
        super().__init__(main)
        self.instances = []

    def _run(self, defn, path):
        for inst in defn.instances:
            inst_defn = type(inst)
            inst_path = path + (inst, )
            self.instances.append(inst_path)
            if callable(self):
                self(inst_path)
            if isdefinition(inst_defn):
                self._run(inst_defn, inst_path)

    def run(self):
        self._run(self.main, tuple())
        self.done()
        return self


class DefinitionPass(Pass):
    def __init__(self, main):
        super().__init__(main)
        self.defns = {}

    def _run(self, defn):
        if not isdefinition(defn):
            return
        for inst in defn.instances:
            inst_defn = type(inst)
            if isdefinition(inst_defn):
                self._run(inst_defn)
        # Call each definition only once.
        id_ = id(defn)
        if id_ not in self.defns:
            self.defns[id_] = defn
            if callable(self):
                self(defn)

    def run(self):
        self._run(self.main)
        self.done()
        return self


class BuildInstanceGraphPass(DefinitionPass):
    def __init__(self, main):
        super().__init__(main)
        self.graph = {}

    def __call__(self, defn):
        if defn not in self.graph:
            self.graph[defn] = []
        for inst in defn.instances:
            inst_defn = type(inst)
            if inst_defn not in self.graph:
                self.graph[inst_defn] = []
            if inst_defn not in self.graph[defn]:
                self.graph[defn].append(inst_defn)

    def done(self):
        graph = []
        for vert, edges in self.graph.items():
            graph.append((vert, edges))
        self.tsortedgraph = tsort(graph)


class InstanceGraphPass(Pass):
    def __init__(self, main):
        super(InstanceGraphPass, self).__init__(main)

        pass_ = BuildInstanceGraphPass(main).run()
        self.tsortedgraph = pass_.tsortedgraph

        if callable(self):
            for vert, edges in self.tsortedgraph:
                self(vert, edges)
