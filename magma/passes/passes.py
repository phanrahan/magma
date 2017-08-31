from ..circuit import isdefinition

__all__ = ['Pass', 'InstancePass', 'DefinitionPass']

# abstract base class
class Pass(object):
    def __init__(self, main):
        self.main = main

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
        return self
    
    def run(self):
         return self._run(self.main)

class DefinitionPass(Pass):
    def __init__(self, main):
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

        return self

    def run(self):
         return self._run(self.main)
