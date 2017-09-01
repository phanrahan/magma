from ..circuit import isdefinition
from .tsort import tsort

__all__ = ['Pass', 'InstancePass', 'DefinitionPass', 'InstanceGraphPass']

# abstract base class
class Pass:
    def __init__(self, main):
        self.main = main

    def run(self):
        self.done()

    def done(self):
        pass


class InstancePass(Pass):
    def __init__(self, main):
        super(InstancePass, self).__init__(main)
        self.instances = []

    def _run(self, definition):
        for instance in definition.instances:
            instancedefinition = type(instance)
            if isdefinition(instancedefinition):
                self._run( instancedefinition )
            self.instances.append(instance)
            if callable(self):
                self(instance)
    
    def run(self):
         self._run(self.main)
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
        name = definition.__name__
        if name not in self.definitions:
            self.definitions[name] = definition
            if callable(self):
                self(definition)

    def run(self):
         self._run(self.main)
         self.done()
         return self


class BuildInstanceGraphPass(InstancePass):
    def __init__(self, main):
        super(BuildInstanceGraphPass, self).__init__(main)
        self.graph = {}

    def __call__(self, instance):
        instancedefinition = type(instance)
        if instancedefinition not in self.graph:
            self.graph[instancedefinition]  = []

        definition = instance.defn # enclosing definition
        if definition not in self.graph:
            self.graph[definition]  = []

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

        for vert, edges in p.tsortedgraph:
            self(vert, edges)

