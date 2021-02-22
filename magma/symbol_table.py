from enum import Enum, auto


class SymbolTableEnum(Enum):
    INLINED = auto()


INLINED = SymbolTableEnum.INLINED


class SymbolTable:
    def get_module_name(self, name):
        raise NotImplementedError()

    def get_instance_name(self, module_name, instance_name):
        raise NotImplementedError()

    def get_port_name(self, module_name, port_name):
        raise NotImplementedError()

    def get_port_name(self, module_name, port_name):
        raise NotImplementedError()

    def get_inlined_instance_name(self, module_name, *instance_names):
        raise NotImplementedError()
