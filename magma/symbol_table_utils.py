import dataclasses
from typing import List, Optional, Sequence, Tuple

from magma.symbol_table import (SymbolTableInterface, SymbolTable,
                                DelegatorSymbolTable, ImmutableSymbolTable,
                                SYMBOL_TABLE_INLINED_INSTANCE,
                                SYMBOL_TABLE_EMPTY)


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

    def has_instance(self, name: str):
        return name in self._instances

    def get_instance(self, name: str):
        return self._instances[name]

    def add_port(self, port: '_Port'):
        assert port.name not in self._ports
        self._ports[port.name] = port

    def get_port(self, name: str):
        return self._ports[name]

    def remove_port(self, name: str):
        del self._ports[name]


@dataclasses.dataclass
class _Instance(_Object):
    type: Optional[_Module] = None

    def __post_init__(self):
        super().__post_init__()
        self._inlines = None

    @property
    def inlined(self):
        return self._inlines is not None

    @property
    def inlines(self):
        if not self.inlined:
            return None
        return self._inlines.copy()

    def inline(self):
        if self.inlined:
            raise ValueError(self)
        self._inlines = []

    def add_inline(self, original, new):
        self._inlines.append((original, new))


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


def _finalize_instance_names(module, instance, table, top=True):
    tail = instance.tail()
    if top:
        if not tail.inlined:
            table.set_instance_name(
                module.name, instance.name, (SYMBOL_TABLE_EMPTY, tail.name))
            return
        table.set_instance_name(
            module.name, instance.name, (SYMBOL_TABLE_INLINED_INSTANCE, ""))
    for original, new in tail.inlines:
        if not new.inlined:
            table.set_inlined_instance_name(
                module.name,
                instance.name,
                original.root.name,
                (SYMBOL_TABLE_EMPTY, new.tail().name))
        else:
            table.set_inlined_instance_name(
                module.name,
                instance.name,
                original.root.name,
                (SYMBOL_TABLE_INLINED_INSTANCE, new.tail().name))
            _finalize_instance_names(module, new, table, top=False)


class _TableProcessor:
    def __init__(self):
        self._modules = {}
        self._scope = 0
        self._finalized = False
        self._uniq_key_map = {}
        self._uniq_key_counter = 0

    def process_table(self, table: SymbolTableInterface):
        self._process_module_names(table.module_names())
        self._process_instance_names(table.instance_names())
        self._process_port_names(table.port_names())
        self._process_instance_types(table.instance_types())
        self._process_inlined_instance_names(table.inlined_instance_names())
        self._scope += 1

    def finalize(self, table: SymbolTableInterface):
        if self._finalized:
            raise Exception("Can not call finalize() multiple times")
        root_modules = list(
            filter(lambda m: m.scope == 0, self._modules.values()))
        for module in root_modules:
            table.set_module_name(module.name, module.tail().name)
            for instance in module.instances:
                _finalize_instance_names(module, instance, table)
                table.set_instance_type(
                    module.name, instance.name, instance.type.name)
            for port in module.ports:
                for tail, modifiers in port.tails():
                    src_port = _PortWrapper(port.name, modifiers).longname()
                    table.set_port_name(module.name, src_port, tail.name)
        self._finalized = True

    def _new_unique_key(self):
        key = f"UNIQ_KEY_{self._uniq_key_counter}"
        self._uniq_key_counter += 1
        return key

    def _get_or_set_uniq_key(self, scope, uniq_key):
        dict_key = (scope, uniq_key)
        try:
            mapped = self._uniq_key_map[dict_key]
        except KeyError:
            mapped = self._new_unique_key()
            self._uniq_key_map[dict_key] = mapped
        return mapped

    def _process_module_names(self, module_names):
        if self._scope != 0:
            unmapped_srcs = {m.name: m
                             for m in self._modules.values()
                             if m.scope == self._scope}
        for in_module_name, out_module_name in module_names.items():
            if self._scope == 0:
                src = _Module(in_module_name, self._scope)
                root = src
                self._modules[src.key()] = src
            else:
                # If this is a new module in this scope, then skip it.
                try:
                    src = self._modules[(self._scope, in_module_name)]
                except KeyError:
                    continue
                del unmapped_srcs[src.name]
                root = src.root
            dst = _Module(out_module_name, self._scope + 1, root=root)
            src.add_rename(_Rename(dst))
            self._modules[dst.key()] = dst
        if self._scope != 0:
            for src in unmapped_srcs.values():
                dst = _Module(src.name, self._scope + 1, root=src.root)
                src.add_rename(_Rename(dst))
                self._modules[dst.key()] = dst

    def _process_instance_names(self, instance_names):
        for key, value in instance_names.items():
            sentinel, out_instance_name = value
            if not (sentinel is SYMBOL_TABLE_EMPTY or
                    sentinel is SYMBOL_TABLE_INLINED_INSTANCE):
                raise ValueError((key, value))
            in_module_name, in_instance_name = key
            # If this is a new module in this scope, then skip it, unless this
            # is the base scope.
            try:
                src_module = self._modules[(self._scope, in_module_name)]
            except KeyError:
                if self._scope == 0:
                    raise
                continue
            dst_module = src_module.get_rename().obj
            if self._scope == 0:
                src_instance = _Instance(in_instance_name, self._scope)
                root_instance = src_instance
                src_module.add_instance(src_instance)
            else:
                if not src_module.has_instance(in_instance_name):
                    continue
                src_instance = src_module.get_instance(in_instance_name)
                root_instance = src_instance.root
            if sentinel is SYMBOL_TABLE_INLINED_INSTANCE:
                src_instance.inline()
            else:
                dst_instance = _Instance(
                    out_instance_name, self._scope + 1, root=root_instance)
                dst_module.add_instance(dst_instance)
                src_instance.add_rename(_Rename(dst_instance))

    def _process_port_names(self, port_names):
        for key, out_port_name in port_names.items():
            in_module_name, in_port_name = key
            # If this is a new module in this scope, then skip it.
            try:
                src_module = self._modules[(self._scope, in_module_name)]
            except KeyError:
                if self._scope == 0:
                    raise
                continue
            dst_module = src_module.get_rename().obj
            modifiers = ()
            if self._scope == 0:
                src_port = _Port(in_port_name, self._scope)
                root_port = src_port
                src_module.add_port(src_port)
            else:
                try:
                    src_port = src_module.get_port(in_port_name)
                except KeyError:
                    dummy_port = _Port(in_port_name, self._scope)
                    src_port = src_module.get_port(dummy_port.wrapper.base)
                    modifiers = dummy_port.wrapper.fields
                root_port = src_port.root
            dst_port = _Port(out_port_name, self._scope + 1, root=root_port)
            dst_module.add_port(dst_port)
            src_port.add_rename(_Rename(dst_port, modifiers))

    def _process_instance_types(self, instance_types):
        for key, out_type in instance_types.items():
            module_name, instance_name = key
            # If this is a new module in this scope, then skip it.
            try:
                module = self._modules[(self._scope, module_name)]
            except KeyError:
                continue
            # If this is a new instance in this module (decl -> defn) then skip
            # it.
            if not module.has_instance(instance_name):
                continue
            instance = module.get_instance(instance_name)
            module_type = self._modules[(self._scope, out_type)]
            instance.type = module_type

    def _process_inlined_instance_names(self, inlined_instance_names):
        items = list(inlined_instance_names.items())
        while items:
            key, value = items.pop()
            module_name, parent_instance_name, child_instance_name = key
            sentinel, new_instance_name_or_key = value
            if not (sentinel is SYMBOL_TABLE_EMPTY or
                    sentinel is SYMBOL_TABLE_INLINED_INSTANCE):
                raise ValueError((key, value))
            src_module = self._modules[(self._scope, module_name)]
            dst_module = src_module.get_rename().obj
            parent_instance_name = self._uniq_key_map.get(
                (self._scope, parent_instance_name), parent_instance_name)
            try:
                parent_instance = src_module.get_instance(parent_instance_name)
            except KeyError:
                items.insert(0, (key, value))
                continue
            child_instance = parent_instance.type.get_instance(
                child_instance_name)
            if not parent_instance.inlined:
                raise ValueError((key, value))
            if sentinel is SYMBOL_TABLE_EMPTY:
                new_instance = _Instance(
                    new_instance_name_or_key, self._scope + 1)
                dst_module.add_instance(new_instance)
            else:
                new_instance_name_or_key = self._get_or_set_uniq_key(
                    self._scope, new_instance_name_or_key)
                new_instance = _Instance(new_instance_name_or_key, self._scope)
                new_instance.inline()
                src_module.add_instance(new_instance)
            new_instance.type = child_instance.type
            parent_instance.add_inline(child_instance, new_instance)


class MasterSymbolTable(ImmutableSymbolTable, DelegatorSymbolTable):
    def __init__(self, tables: Sequence[SymbolTableInterface]):
        super().__init__(SymbolTable())
        processor = _TableProcessor()
        for table in tables:
            processor.process_table(table)
        processor.finalize(self._underlying)


class SymbolQueryInterface:

    class InlinedLeafInstanceError(Exception):
        pass

    @dataclasses.dataclass
    class _Inst:
        name: str
        type: str

    def __init__(self, table: SymbolTableInterface):
        self._table = table

    def get_module_name(self, module_name):
        return self._table.get_module_name(module_name)

    def _get_inlined_instance_name_impl(
            self, module: str, parent_inst: _Inst, insts: List[_Inst]):
        if not insts:
            return []
        child_inst = insts[0]
        sentinel, new_name_or_key = self._table.get_inlined_instance_name(
            module, parent_inst.name, child_inst.name)
        if sentinel is SYMBOL_TABLE_EMPTY:
            name = new_name_or_key
            insts = insts[1:]
            return [name] + self._get_instance_name_impl(child_inst.type, insts)
        if sentinel is SYMBOL_TABLE_INLINED_INSTANCE:
            insts = insts[1:]
            if not insts:
                raise SymbolQueryInterface.InlinedLeafInstanceError()
            key = SymbolQueryInterface._Inst(new_name_or_key, None)
            return self._get_inlined_instance_name_impl(module, key, insts)
        raise ValueError(sentinel)

    def _get_instance_name_impl(self, module: str, insts: List[_Inst]):
        if not insts:
            return []
        inst = insts[0]
        sentinel, name = self._table.get_instance_name(module, inst.name)
        if sentinel is SYMBOL_TABLE_EMPTY:
            return [name] + self._get_instance_name_impl(inst.type, insts[1:])
        if sentinel is SYMBOL_TABLE_INLINED_INSTANCE:
            insts = insts[1:]
            if not insts:
                raise SymbolQueryInterface.InlinedLeafInstanceError()
            return self._get_inlined_instance_name_impl(module, inst, insts)
        raise ValueError(sentinel)

    def _get_types(self, module: str, insts: List[str]):
        curr_module = module
        out = []
        for inst in insts:
            curr_module = self._table.get_instance_type(curr_module, inst)
            out.append(curr_module)
        return out

    def get_instance_name(self, path: str) -> Optional[str]:
        module, *insts = path.split(".")
        if not insts:
            raise ValueError(path)
        insts = [SymbolQueryInterface._Inst(inst, t)
                 for inst, t in zip(insts, self._get_types(module, insts))]
        new_path = [self._table.get_module_name(module)]
        inst_path = self._get_instance_name_impl(module, insts)
        new_path += inst_path
        return ".".join(new_path)


def make_master_symbol_table(json_filenames: Sequence[str]):
    # TODO(rsetaluri): Make this lazy.
    symbol_tables = []
    for filename in json_filenames:
        with open(filename, "r") as f:
            table = SymbolTable.from_json(f.read())
            symbol_tables.append(table)
    return MasterSymbolTable(symbol_tables)
