import dataclasses
from typing import Sequence, Tuple

from magma.symbol_table import SymbolTableInterface, SymbolTable


def _get_mapped_module_name(module_name, local, total):
    try:
        return local[module_name]
    except KeyError:
        pass
    try:
        return total[module_name]
    except KeyError:
        pass
    return module_name


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
            return _PortWrapper(parts[0], tuple())
        return _PortWrapper(parts[0], tuple(parts[1:]))


class _TableProcessor:
    def __init__(self):
        self._first = True
        self._module_names = {}
        self._module_names_lookup = {}
        self._instance_names = {}
        self._instance_names_lookup = {}
        self._port_names = {}
        self._port_names_lookup = {}

    def process_table(self, table: SymbolTableInterface):
        self._process_module_names(table.module_names())
        self._process_instance_names(
            table.instance_names(), table.module_names())
        self._process_port_names(table.port_names(), table.module_names())
        self._first = False

    def update_master(self, master: 'MasterSymbolTable'):
        for in_module_name, out_module_name in self._module_names.items():
            SymbolTable.set_module_name(master, in_module_name, out_module_name)
        for key, value in self._instance_names.items():
            in_module_name, in_instance_name = key
            _, out_instance_name = value
            SymbolTable.set_instance_name(
                master, in_module_name, in_instance_name, out_instance_name)
        for key, value in self._port_names.items():
            in_module_name, in_port_name = key
            out_module_name, out_port_name = value
            SymbolTable.set_port_name(
                master, in_module_name, in_port_name.longname(),
                out_module_name, out_port_name.longname())

    def _process_module_names(self, module_names):
        for in_module_name, out_module_name in module_names.items():
            try:
                update_key = self._module_names_lookup.pop(in_module_name)
            except KeyError:
                if in_module_name in self._module_names:
                    err = Exception(
                        f"Duplicate mapping of module name {in_module_name}")
                    raise err from None
                if not self._first:
                    raise Exception(
                        f"Unexpected module name {in_module_name}") from None
                update_key = in_module_name
            self._module_names[update_key] = out_module_name
            self._module_names_lookup[out_module_name] = update_key

    def _process_instance_names(self, instance_names, module_names):
        for key, out_instance_name in instance_names.items():
            in_module_name, _ = key
            out_module_name = _get_mapped_module_name(
                in_module_name, module_names, self._module_names)
            try:
                update_key = self._instance_names_lookup.pop(key)
            except KeyError:
                update_key = key
            new_value = out_module_name, out_instance_name
            self._instance_names[update_key] = new_value
            self._instance_names_lookup[new_value] = update_key

    def _process_port_names(self, port_names, module_names):
        to_del = []
        for key, (_, out_port_name) in port_names.items():
            in_module_name, in_port_name = key
            out_module_name = _get_mapped_module_name(
                in_module_name, module_names, self._module_names)
            in_port = _PortWrapper.make(in_port_name)
            out_port = _PortWrapper.make(out_port_name)

            lookup_type = None
            try:
                lookup = self._port_names_lookup[in_module_name, in_port]
                lookup_type = 0
            except KeyError:
                try:
                    lookup = self._port_names_lookup[
                        in_module_name, _PortWrapper(in_port.base, ())]
                    lookup_type = 1
                except KeyError:
                    lookup_type = 2
            if lookup_type == 0:
                key = lookup
                value = out_module_name, out_port
            elif lookup_type == 1:
                to_del.append(
                    (lookup, (in_module_name, _PortWrapper(in_port.base, ()))))
                key = lookup[0], _PortWrapper(lookup[1].base, in_port.fields)
                value = out_module_name, out_port
            elif lookup_type == 2:
                key = in_module_name, in_port
                value = out_module_name, out_port
            else:
                raise NotImplementedError(lookup_type)
            self._port_names[key] = value
            self._port_names_lookup[value] = key

        for forward, backward in to_del:
            try:
                del self._port_names[forward]
            except KeyError:
                pass
            try:
                del self._port_names_lookup[backward]
            except KeyError:
                pass


class MasterSymbolTable(SymbolTable):
    def __init__(self, tables: Sequence[SymbolTableInterface]):
        super().__init__()
        processor = _TableProcessor()
        for table in tables:
            processor.process_table(table)
        processor.update_master(self)

    def set_module_name(self,
                        in_module_name: str,
                        out_module_name: str) -> None:
        raise Exception("Setting not allowed on master symbol table")

    def set_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_instance_name: str) -> None:
        raise Exception("Setting not allowed on master symbol table")

    def set_port_name(self,
                      in_module_name: str,
                      in_port_name: str,
                      out_module_name: str,
                      out_port_name: str) -> None:
        raise Exception("Setting not allowed on master symbol table")


def make_master_symbol_table(json_filenames: Sequence[str]):
    # TODO(rsetaluri): Make this lazy.
    symbol_tables = []
    for filename in json_filenames:
        with open(filename, "r") as f:
            table = SymbolTable.from_json(f.read())
            symbol_tables.append(table)
    return MasterSymbolTable(symbol_tables)
