import dataclasses
from typing import Any, Callable, Iterable, Mapping, Union

from magma.array import Array, ArrayMeta
from magma.backend.mlir.common import make_unique_name, replace_all
from magma.circuit import Circuit, DefineCircuitKind
from magma.ref import Ref, ArrayRef, TupleRef
from magma.t import Kind, Type
from magma.tuple import TupleMeta, Tuple as m_Tuple


ModuleLike = Union[DefineCircuitKind, Circuit]


_VALUE_OR_TYPE_TO_STRING_REPLACEMENTS = {
    "(": "_",
    ")": "",
    "[": "_",
    "]": "",
    " ": "",
    ",": "_",
    "=": "_",
    ".": "_",
}


def contains_tuple(T: Kind):
    if isinstance(T, TupleMeta):
        return True
    if isinstance(T, ArrayMeta):
        return contains_tuple(T.T)
    return False


def value_or_type_to_string(value_or_type: Union[Type, Kind]):
    if isinstance(value_or_type, Type):
        s = value_or_type.name.qualifiedname("_")
    else:
        s = str(value_or_type)
    return replace_all(s, _VALUE_OR_TYPE_TO_STRING_REPLACEMENTS)


@dataclasses.dataclass(frozen=True)
class ValueWrapper:
    id: str = dataclasses.field(default_factory=make_unique_name, init=False)
    name: str
    T: Kind

    def is_input(self) -> bool:
        return self.T.is_input()

    def is_output(self) -> bool:
        return self.T.is_output()

    def is_mixed(self) -> bool:
        return self.T.is_mixed()

    def __iter__(self) -> Iterable['ValueWrapper']:
        if isinstance(T, TupleMeta):
            return (
                ValueWrapper(f"{value_wrapper.name}_{key}", TT)
                for key, TT in self.T.field_dict.items()
            )
        if isinstance(T, ArrayMeta):
            return (
                ValueWrapper(f"{value_wrapper.name}[{key}]", self.T.T)
                for index in range(T.N)
            )
        raise NotImplementedError(f"{self} is not iterable")


ValueOrValueWrapper = Union[Type, ValueWrapper]


def visit_value_or_value_wrapper_by_direction(
        value_or_value_wrapper: ValueOrValueWrapper,
        input_visitor: Callable[[Type], Any],
        output_visitor: Callable[[Type], Any],
        **kwargs):

    def descend(v):
        if not isinstance(v, (m_Tuple, Array)):
            raise TypeError(value)
        for item in v:
            visit_value_or_value_wrapper_by_direction(
                item, input_visitor, output_visitor, **kwargs)

    flatten_all_tuples = kwargs.get("flatten_all_tuples", False)

    if flatten_all_tuples and contains_tuple(type(value_or_value_wrapper)):
        return descend(value_or_value_wrapper)
    if value_or_value_wrapper.is_input():
        return input_visitor(value_or_value_wrapper)
    if value_or_value_wrapper.is_output():
        return output_visitor(value_or_value_wrapper)
    if value_or_value_wrapper.is_mixed():
        return descend(value_or_value_wrapper)

    raise TypeError(value_or_value_wrapper)


class InstanceWrapper:

    @dataclasses.dataclass(frozen=True)
    class _Interface:
        ports: Mapping[str, ValueWrapper]

    def __init__(
            self,
            name: str,
            ports: Mapping[str, Kind],
            attrs: Mapping[str, Any]):
        self._name = name
        ports = {name: ValueWrapper(name, T) for name, T in ports.items()}
        self._interface = InstanceWrapper._Interface(ports)
        self._attrs = attrs
        for name, value in ports.items():
            setattr(self, name, value)

    def __repr__(self) -> str:
        return f"InstanceWrapper({self.name})"

    @property
    def name(self) -> str:
        return self._name

    @property
    def interface(self) -> _Interface:
        return self._interface

    @property
    def attrs(self) -> Mapping[str, Any]:
        return self._attrs.copy()


def safe_root(ref: Ref) -> Ref:
    """Returns the root ref of @ref."""
    # TODO(rsetaluri): This should be able to return `ref.root()`, but depends
    # on #990.
    parent = ref
    if isinstance(ref, ArrayRef):
        parent = ref.array.name
    elif isinstance(ref, TupleRef):
        parent = ref.tuple.name
    if parent is ref:
        return ref
    return safe_root(parent)
