from magma.protocol_type import MagmaProtocol, MagmaProtocolMeta
from magma.ref import PortViewRef
from magma.t import Out


class PortViewMeta(MagmaProtocolMeta):
    def _to_magma_(cls):
        return cls.T

    def _qualify_magma_(cls, direction):
        return cls[cls.T.qualify(direction)]

    def _flip_magma_(cls):
        return cls[cls.T.flip()]

    def __getitem__(cls, T):
        return type(cls)(f"PortView{T}", (cls, ), {"T": T})


class PortView(MagmaProtocol, metaclass=PortViewMeta):
    def _get_magma_value_(self):
        return self._magma_value

    def __init__(self, port, parent):
        self.port = port
        self.parent = parent
        self._magma_value = Out(type(port))(name=PortViewRef(self))

    def __getitem__(self, key):
        port = self.port
        try:
            item = port[key]
        except KeyError:
            raise Exception(f"Can only use getitem with arrays and "
                            f"tuples not {type(self.port)}")
        return PortView[type(item)](item, self.parent)

    def __getattr__(self, key):
        port = self.port
        try:
            attr = getattr(port, key)
        except AttributeError:
            return object.__getattribute__(self, key)
        return PortView[type(attr)](attr, self.parent)

    def get_hierarchical_coreir_select(self):
        curr = self.parent
        path = curr.inst().name + ";"
        while isinstance(curr.parent, InstView):
            path = curr.parent.inst().name + ";" + path
            curr = curr.parent
        return path

    def root(self):
        curr = self.parent
        while isinstance(curr.parent, InstView):
            curr = curr.parent
        return curr

    def __str__(self):
        return (self.get_hierarchical_coreir_select() +
                self.port.name.qualifiedname())

    def __iter__(self):
        self.__iter = iter(self.port)
        return self

    def __len__(self):
        return len(self.port)

    def __next__(self):
        n = next(self.__iter)
        return PortView[type(n)](n, self.parent)


class InstView:
    def __init__(self, inst, parent=None):
        self._inst = inst
        self.circuit = type(inst)
        self.instance_map = None
        if hasattr(self.circuit, "instances"):
            self.instance_map = {instance.name: instance for instance in
                                 self.circuit.instances}
        self.parent = parent

    def __getattr__(self, attr):
        try:
            if attr in self.circuit.interface.ports.keys():
                port = self._inst.interface.ports[attr]
                return PortView[type(port)](port, self)
            elif attr in self.instance_map:
                return InstView(self.instance_map[attr], self)
        except AttributeError:
            return object.__getattribute__(self, attr)

    def inst(self):
        return self._inst

    def defn(self):
        return None
