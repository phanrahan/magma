from ..is_definition import isdefinition
from .tsort import tsort

__all__ = ['Pass', 'InstancePass', 'DefinitionPass', 'InstanceGraphPass']

# abstract base class
class Pass(object):
    def __init__(self, main):
        self.main = main

    def run(self):
        self.done()
        return self

    def done(self):
        pass


class InstancePass(Pass):
    def __init__(self, main):
        super(InstancePass, self).__init__(main)
        self.instances = []

    def _run(self, definition, path):
        for instance in definition.instances:
            instancedefinition = type(instance)
            instpath = path + (instance, )
            self.instances.append(instpath)
            if callable(self):
                self(instpath)
            if isdefinition(instancedefinition):
                self._run( instancedefinition, instpath )
    
    def run(self):
         self._run(self.main, tuple())
         self.done()
         return self

class DefinitionPass(Pass):
    def __init__(self,main):
        super(DefinitionPass, self).__init__(main)
        self.definitions = {}

    def _run(self, definition):
        for instance in definition.instances:
            instancedefinition = type(instance)
            if isdefinition(instancedefinition):
                self._run( instancedefinition )

        # call each definition only once
        id_ = id(definition)
        if id_ not in self.definitions:
            self.definitions[id_] = definition
            if callable(self):
                self(definition)

    def run(self):
         self._run(self.main)
         self.done()
         return self


class BuildInstanceGraphPass(DefinitionPass):
    def __init__(self, main):
        super(BuildInstanceGraphPass, self).__init__(main)
        self.graph = {}

    def __call__(self, definition):
        if definition not in self.graph:
            self.graph[definition]  = []
        for instance in definition.instances:
            instancedefinition = type(instance)
            if instancedefinition not in self.graph:
                self.graph[instancedefinition]  = []
            if instancedefinition not in self.graph[definition]:
                #print('Adding',definition.name, instancedefinition.name)
                self.graph[definition].append(instancedefinition)

    def done(self):
        graph = []
        for vert, edges in self.graph.items():
            graph.append((vert, edges))
        self.tsortedgraph = tsort(graph)


class InstanceGraphPass(Pass):
    def __init__(self, main):
        super(InstanceGraphPass, self).__init__(main)

        p = BuildInstanceGraphPass(main).run()
        self.tsortedgraph = p.tsortedgraph

        if callable(self):
            for vert, edges in self.tsortedgraph:
                self(vert, edges)

