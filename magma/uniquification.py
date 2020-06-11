from dataclasses import dataclass
from enum import Enum, auto
from .is_definition import isdefinition
from .logging import root_logger
from .passes import DefinitionPass


_logger = root_logger()


class MultipleDefinitionException(Exception):
    pass


class UniquificationMode(Enum):
    WARN = auto()
    ERROR = auto()
    UNIQUIFY = auto()


@dataclass(frozen=True)
class _HashStruct:
    defn_repr: str
    is_verilog: bool
    verilog_str: bool


def _make_hash_struct(definition):
    repr_ = repr(definition)
    if hasattr(definition, "verilogFile") and definition.verilogFile:
        return _HashStruct(repr_, True, definition.verilogFile)
    return _HashStruct(repr_, False, "")


def _hash(definition):
    hash_struct = _make_hash_struct(definition)
    return hash(hash_struct)


class UniquificationPass(DefinitionPass):
    def __init__(self, main, mode):
        super().__init__(main)
        self.mode = mode
        self.seen = {}
        self.original_names = {}

    def __call__(self, definition):
        name = definition.name
        key = _hash(definition)

        seen = self.seen.setdefault(name, {})
        if key not in seen:
            if self.mode is UniquificationMode.UNIQUIFY and len(seen) > 0:
                suffix = "_unq" + str(len(seen))
                new_name = name + suffix
                type(definition).rename(definition, new_name)
                for module in definition.bind_modules:
                    type(module).rename(module, module.name + suffix)
            seen[key] = [definition]
        else:
            if self.mode is not UniquificationMode.UNIQUIFY:
                assert seen[key][0].name == name
            elif name != seen[key][0].name:
                new_name = seen[key][0].name
                type(definition).rename(definition, new_name)
                for x, y in zip(seen[key][0].bind_modules,
                                definition.bind_modules):
                    type(y).rename(y, x.name)
            seen[key].append(definition)

    def run(self):
        super().run()
        duplicated = []
        for name, definitions in self.seen.items():
            if len(definitions) > 1:
                duplicated.append((name, definitions))
        UniquificationPass.handle(duplicated, self.mode)

    @staticmethod
    def handle(duplicated, mode):
        if len(duplicated):
            msg = f"Multiple definitions: {[name for name, _ in duplicated]}"
            if mode is UniquificationMode.ERROR:
                error(msg)
                raise MultipleDefinitionException([name for name, _ in duplicated])
            elif mode is UniquificationMode.WARN:
                warning(msg)


def _get_mode(mode_or_str):
    if isinstance(mode_or_str, str):
        try:
            return UniquificationMode[mode_or_str]
        except KeyError as e:
            modes = [k for k in UniquificationMode.__members__]
            raise ValueError(f"Valid uniq. modes are {modes}")
    if isinstance(mode_or_str, UniquificationMode):
        return mode_or_str
    raise NotImplementedError(f"Unsupported type: {type(mode_or_str)}")


# This pass runs uniquification according to @mode and returns a dictionary
# mapping any renamed circuits to their original names. If @mode is ERROR or
# WARN the returned dictionary should be empty.
def uniquification_pass(circuit, mode_or_str):
    mode = _get_mode(mode_or_str)
    pass_ = UniquificationPass(circuit, mode)
    pass_.run()
    return pass_.original_names
