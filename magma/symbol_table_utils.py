import dataclasses
from typing import List, Optional, Sequence, Tuple

from magma.symbol_table import (SymbolTableInterface, SymbolTable,
                                DelegatorSymbolTable, ImmutableSymbolTable)


@dataclasses.dataclass
class _Object:
    name: str
    scope: int
    root: Optional['_Object'] = None

    def __post_init__(self):
        self._renames: List[_Rename] = []

    @property
    def renames(self):
        return self._renames.copy()

    def root_or_self(self):
        if self.root is not None:
            return self.root
        return self

    def tail(self):
        if not self._renames:
            return self
        if len(self._renames) == 1:
            return self._renames[0].obj.tail()
        raise ValueError(self)

    def key(self):
        return (self.scope, self.name)

    def add_rename(self, rename: '_Rename'):
        self._renames.append(rename)

    def print_tree(self, print_self=True, indent=0):
        if print_self:
            print (" " * indent + repr(self))
        for rename in self._renames:
            rename.obj.print_tree(indent=indent + 1)


@dataclasses.dataclass
class _Rename:
    obj: _Object
    modifiers: Tuple[str] = ()


@dataclasses.dataclass
class _Module(_Object):
    def __post_init__(self):
        super().__post_init__()
        self._instances: List['_Instance'] = {}
        self._ports: List['_Port'] = {}

    @property
    def instances(self):
        return self._instances.values()

    @property
    def ports(self):
        return self._ports.values()

    def get_rename(self):
        if len(self._renames) != 1:
            raise ValueError(self)
        return self._renames[0]

    def add_instance(self, instance: '_Instance'):
        assert instance.name not in self._instances
        self._instances[instance.name] = instance

    def get_instance(self, name: str):
        return self._instances[name]

    def add_port(self, port: '_Port'):
        assert port.name not in self._ports
        self._ports[port.name] = port

    def get_port(self, name: str):
        return self._ports[name]

    def remove_port(self, name: str):
        self._ports.pop(name)


@dataclasses.dataclass
class _Instance(_Object):
    pass


@dataclasses.dataclass(eq=True, frozen=True)
class _PortWrapper:
    base: str
    fields: Tuple[str]

    def longname(self):
        if not self.fields:
            return self.base
        return self.base + "." + ".".join(self.fields)

    @staticmethod
    def make(longname: str):
        parts = longname.split(".")
        if not len(parts) > 0:
            raise ValueError(longname)
        if len(parts) == 1:
            return _PortWrapper(parts[0], ())
        return _PortWrapper(parts[0], tuple(parts[1:]))


@dataclasses.dataclass
class _Port(_Object):
    def __post_init__(self):
        super().__post_init__()
        self._wrapper = _PortWrapper.make(self.name)

    @property
    def wrapper(self):
        return self._wrapper

    def tails(self):
        if not self._renames:
            return [(self, ())]
        tails = []
        for rename in self._renames:
            sub_tails = rename.obj.tails()
            for obj, modifiers in sub_tails:
                tails.append((obj, rename.modifiers + modifiers))
        return tails


class _TableProcessor:
    def __init__(self):
        self._modules = {}
        self._index = 0

    def process_table(self, table: SymbolTableInterface):
        self._process_module_names(table.module_names())
        self._process_instance_names(table.instance_names())
        self._process_port_names(table.port_names())
        self._index += 1

    def finalize(self, table: SymbolTableInterface):
        root_modules = list(
            filter(lambda m: m.scope == 0, self._modules.values()))
        for module in root_modules:
            table.set_module_name(module.name, module.tail().name)
            for instance in module.instances:
                table.set_instance_name(
                    module.name, instance.name, instance.tail().name)
            for port in module.ports:
                for tail, modifiers in port.tails():
                    src_port = _PortWrapper(port.name, modifiers).longname()
                    table.set_port_name(module.name, src_port, tail.name)

    def _process_module_names(self, module_names):
        for in_module_name, out_module_name in module_names.items():
            if self._index == 0:
                src = _Module(in_module_name, self._index)
                root = src
                self._modules[src.key()] = src
            else:
                src = self._modules[(self._index, in_module_name)]
                root = src.root
            dst = _Module(out_module_name, self._index + 1, root=root)
            src.add_rename(_Rename(dst))
            self._modules[dst.key()] = dst

    def _process_instance_names(self, instance_names):
        for key, out_instance_name in instance_names.items():
            in_module_name, in_instance_name = key
            src_module = self._modules[(self._index, in_module_name)]
            dst_module = src_module.get_rename().obj
            if self._index == 0:
                src_instance = _Instance(in_instance_name, self._index)
                root_instance = src_instance
                src_module.add_instance(src_instance)
            else:
                src_instance = src_module.get_instance(in_instance_name)
                root_instance = src_instance.root
            dst_instance = _Instance(
                out_instance_name, self._index + 1, root=root_instance)
            dst_module.add_instance(dst_instance)
            src_instance.add_rename(_Rename(dst_instance))

    def _process_port_names(self, port_names):
        for key, out_port_name in port_names.items():
            in_module_name, in_port_name = key
            src_module = self._modules[(self._index, in_module_name)]
            dst_module = src_module.get_rename().obj
            modifiers = ()
            if self._index == 0:
                src_port = _Port(in_port_name, self._index)
                root_port = src_port
                src_module.add_port(src_port)
            else:
                try:
                    src_port = src_module.get_port(in_port_name)
                except KeyError:
                    dummy_port = _Port(in_port_name, self._index)
                    src_port = src_module.get_port(dummy_port.wrapper.base)
                    modifiers = dummy_port.wrapper.fields
                root_port = src_port.root
            dst_port = _Port(out_port_name, self._index + 1, root=root_port)
            dst_module.add_port(dst_port)
            src_port.add_rename(_Rename(dst_port, modifiers))


class MasterSymbolTable(DelegatorSymbolTable, ImmutableSymbolTable):
    def __init__(self, tables: Sequence[SymbolTableInterface]):
        super().__init__(SymbolTable())
        processor = _TableProcessor()
        for table in tables:
            processor.process_table(table)
        processor.finalize(self._underlying)


def make_master_symbol_table(json_filenames: Sequence[str]):
    # TODO(rsetaluri): Make this lazy.
    symbol_tables = []
    for filename in json_filenames:
        with open(filename, "r") as f:
            table = SymbolTable.from_json(f.read())
            symbol_tables.append(table)
    return MasterSymbolTable(symbol_tables)
