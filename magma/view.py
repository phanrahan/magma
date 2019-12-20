import magma as m


class PortView:
    def __init__(self, port, parent):
        self.port = port
        self.parent = parent
        self.name = self

    def __getitem__(self, key):
        if not isinstance(self.port, (m.ArrayType, m.TupleType)):
            raise Exception(f"Can only use getitem with arrays and "
                            f"tuples not {type(self.port)}")

        return PortView(self.port[key], self)

    def __getattr__(self, key):
        if isinstance(self.port, m.TupleType):
            if key in self.port.Ks:
                return PortView(getattr(self.port, key), self.parent)
        return object.__getattribute__(self, key)


class InstView:
    def __init__(self, inst, parent=None):
        self.inst = inst
        self.circuit = type(inst)
        self.instance_map = None
        if hasattr(self.circuit, "instances"):
            self.instance_map = {instance.name: instance for instance in
                                 self.circuit.instances}
        self.parent = parent

    def __getattr__(self, attr):
        try:
            if attr in self.circuit.interface.ports.keys():
                return PortView(self.circuit.interface.ports[attr], self)
            elif attr in self.instance_map:
                return InstanceVieW(self.instance_map[attr], self)
        except AttributeError:
            pass
        return object.__getattribute__(self, attr)
