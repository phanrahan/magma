class PortView:
    def __init__(self, port, parent):
        self.port = port
        self.parent = parent
        self.name = self

    def __getitem__(self, key):
        port = self.port
        try:
            item = port[key]
        except KeyError:
            raise Exception(f"Can only use getitem with arrays and "
                            f"tuples not {type(self.port)}")
        return PortView(item, self.parent)

    def __getattr__(self, key):
        port = self.port
        try:
            attr = getattr(port, key)
        except AttributeError:
            return object.__getattribute__(self, key)
        return PortView(attr, self.parent)


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
                return InstView(self.instance_map[attr], self)
        except AttributeError:
            return object.__getattribute__(self, attr)
