from collections import namedtuple

class Scope:
    def __init__(self, **kwargs):
        if 'parent' in kwargs:
            self.val = kwargs['parent'].val + '/'
        else:
            self.val = '/'
        if 'const' in kwargs:
            self.val += kwargs['const']
        elif 'instance' in kwargs:
            inst = kwargs['instance']
            self.val += type(inst).__name__ + '.' + inst.name

    def value(self):
        return self.val

    def __eq__(self, rhs):
        return self.val == rhs.val

    def __hash__(self):
        return hash(self.val)

QualifiedBit = namedtuple('QualifiedBit', ['bit', 'scope'])
QualifiedInstance = namedtuple('QualifiedInstance', ['instance', 'scope'])
