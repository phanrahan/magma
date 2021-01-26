from dataclasses import dataclass
from enum import Enum, auto

from magma.is_definition import isdefinition
from magma.logging import root_logger
from magma.passes.passes import CircuitPass


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


def _make_hash_struct(ckt):
    repr_ = repr(ckt)
    if hasattr(ckt, "verilogFile") and ckt.verilogFile:
        return _HashStruct(repr_, True, ckt.verilogFile)
    return _HashStruct(repr_, False, "")


def _hash(ckt):
    hash_struct = _make_hash_struct(ckt)
    return hash(hash_struct)


class Uniquifier:
    def __init__(self, mode, seen, keys):
        self._mode = mode
        self._seen = seen
        self._keys = keys
        self._cache = {}

    def equivalent(self, ckt):
        key = self._keys[ckt]
        return self._seen[ckt.name][key].copy()

    def _index_impl(self, ckt):
        seen = self._seen[ckt.name]
        key = self._keys[ckt]
        return list(seen.keys()).index(key)

    def index(self, ckt):
        try:
            return self._cache[ckt]
        except KeyError:
            pass
        index = self._index_impl(ckt)
        self._cache[ckt] = index
        return index

    def update(self, main):
        # NOTE: very unperformant and hacky!
        pass_ = UniquificationPreprocessPass(main)
        pass_.run()
        self._reset(pass_.seen, pass_.key_cache)

    def _reset(self, seen, keys):
        self._seen = seen
        self._keys = keys
        self._cache = {}


class UniquificationPreprocessPass(CircuitPass):
    def __init__(self, main):
        super().__init__(main)
        self._seen = {}
        self._key_cache = {}

    @property
    def seen(self):
        return self._seen.copy()

    @property
    def key_cache(self):
        return self._key_cache.copy()

    def __call__(self, ckt):
        try:
            key = self._key_cache[ckt]
        except KeyError:
            pass
        key = _hash(ckt)
        self._key_cache[ckt] = key
        seen = self._seen.setdefault(ckt.name, {})
        equivalent = seen.setdefault(key, [])
        equivalent.append(ckt)


def _get_mode(mode_or_str):
    if isinstance(mode_or_str, UniquificationMode):
        return mode_or_str
    try:
        return UniquificationMode[mode_or_str]
    except KeyError as e:
        modes = [k for k in UniquificationMode.__members__]
        raise ValueError(f"Valid uniq. modes are {modes}, got {mode_or_str}")


# This pass runs uniquification according to @mode and returns a dictionary
# mapping any renamed circuits to their original names. If @mode is ERROR or
# WARN the returned dictionary should be empty.
def uniquification_pass(main, mode_or_str):
    mode = _get_mode(mode_or_str)
    pass_ = UniquificationPreprocessPass(main)
    pass_.run()
    return Uniquifier(mode, pass_.seen, pass_.key_cache)
