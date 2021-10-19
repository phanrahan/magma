import abc
import contextlib
import dataclasses
from typing import List, Optional, Tuple

from common import Stack, WithId, default_list_field
from printer_base import PrinterBase


class MlirTypeMeta(abc.ABCMeta):
    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        if name == "MlirType":
            return cls
        dialect = maybe_peek_dialect()
        if dialect is not None:
            dialect.register_type(cls)
        return cls


class MlirType(metaclass=MlirTypeMeta):
    @abc.abstractmethod
    def emit(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class MlirValue:
    type: MlirType
    name: str


@dataclasses.dataclass
class MlirBlock(WithId):
    operations: List['MlirOp'] = default_list_field(init=False)
    arguments: List[MlirValue] = default_list_field(init=False)

    def print(self, printer: PrinterBase):
        for operation in self.operations:
            operation.print(printer)

    def add_operation(self, operation: 'MlirOp'):
        self.operations.append(operation)


_block_stack = Stack()


def get_block_stack() -> Stack:
    global _block_stack
    return _block_stack


@contextlib.contextmanager
def push_block(block):
    get_block_stack().push(block)
    try:
        yield
    finally:
        get_block_stack().pop()


@dataclasses.dataclass
class MlirRegion(WithId):
    blocks: List[MlirBlock] = default_list_field(init=False)

    def print(self, printer: PrinterBase):
        for block in self.blocks:
            block.print(printer)


class MlirOpMeta(abc.ABCMeta):
    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        try:
            block = get_block_stack().peek()
        except IndexError:
            pass
        else:
            block.add_operation(obj)
        return obj

    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        if name == "MlirOp":
            return cls
        dialect = maybe_peek_dialect()
        if dialect is not None:
            dialect.register_op(cls)
        return cls


@dataclasses.dataclass
class MlirOp(WithId, metaclass=MlirOpMeta):
    regions: List[MlirRegion] = default_list_field(init=False)
    operands: List[MlirValue] = default_list_field(init=False)
    results: List[MlirValue] = default_list_field(init=False)

    def print(self, printer: PrinterBase):
        self.print_op(printer)
        if not self.regions:
            printer.flush()
            return
        printer.print(" {")
        printer.flush()
        printer.push()
        for region in self.regions:
            region.print(printer)
        printer.pop()
        printer.print_line("}")

    @abc.abstractmethod
    def print_op(self, printer: PrinterBase):
        raise NotImplementedError()


class MlirDialect:
    def __init__(self, name: str):
        self._name = name
        self._klasses = {}

    @property
    def name(self) -> str:
        return self._name

    def _register(self, cls: type, arg_name: str, base: type):
        if not issubclass(cls, base):
            raise TypeError(f"{arg_name} must be subclass of {base.__name__}")
        name = cls.__name__
        if name in self._klasses:
            raise RuntimeError(f"{name} already part of {self.name} dialect")
        self._klasses[name] = cls
        setattr(self, name, cls)

    def register_op(self, op: type):
        self._register(op, "op", MlirOp)

    def register_type(self, t: type):
        self._register(t, "t", MlirType)


_dialect_stack = Stack()


def get_dialect_stack() -> Stack:
    global _dialect_stack
    return _dialect_stack


def begin_dialect(dialect: MlirDialect):
    get_dialect_stack().push(dialect)


def end_dialect():
    get_dialect_stack().pop()


def maybe_peek_dialect() -> Optional[MlirDialect]:
    stack = get_dialect_stack()
    try:
        return stack.peek()
    except IndexError:
        return None
