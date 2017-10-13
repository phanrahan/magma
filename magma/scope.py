from collections import namedtuple

class Scope:
    def __init__(self, **kwargs):
        self.inst = None
        self.parent = None
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
            self.val = self.parent.val 
            if self.val is not "/":
                self.val += '/'
        else:
            self.val = '/'

        if 'instance' in kwargs:
            self.inst = kwargs['instance']
            self.val += type(self.inst).__name__ + '.' + self.inst.name

    def inst_scope():
        return self.inst is not None

    def value(self):
        return self.val

    def __eq__(self, rhs):
        return self.val == rhs.val

    def __hash__(self):
        return hash(self.val)

QualifiedBit = namedtuple('QualifiedBit', ['bit', 'scope'])
QualifiedInstance = namedtuple('QualifiedInstance', ['instance', 'scope'])
