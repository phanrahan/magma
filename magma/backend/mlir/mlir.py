import abc
import contextlib
import dataclasses
import functools
from typing import List, Mapping, Optional, Tuple
import weakref

from magma.backend.mlir.common import WithId, default_field, constant
from magma.backend.mlir.print_opts import PrintOpts
from magma.backend.mlir.printer_base import PrinterBase
from magma.common import Stack, epilogue


OptionalWeakRef = Optional[weakref.ReferenceType]


class DialectKind(abc.ABCMeta):
    def __new__(metacls, name, bases, dct):
        cls = super().__new__(metacls, name, bases, dct)
        try:
            maybe_peek_dialect
        except NameError:
            return cls
        dialect = maybe_peek_dialect()
        if dialect is not None:
            cls._register_(dialect)
        return cls


class MlirAttributeMeta(DialectKind):
    def _register_(cls, dialect):
        dialect.register_attribute(cls)


class MlirAttribute(metaclass=MlirAttributeMeta):
    @abc.abstractmethod
    def emit(self) -> str:
        raise NotImplementedError()


class MlirLocation(MlirAttribute):
    pass


_location_stack = Stack()


def get_location_stack() -> Stack:
    global _location_stack
    return _location_stack


@contextlib.contextmanager
def push_location(location: MlirLocation):
    get_location_stack().push(location)
    try:
        yield
    finally:
        get_location_stack().pop()


def _default_location():
    # NOTE(rsetaluri): Due to the circular import dependency on the builtin
    # dialect for the default (unknown) location, we need to use a dynamic
    # import. Fortunately, this is used in a dataclass field factory function
    # anyway, and we can cache it so it will be little to no overhead.
    from magma.backend.mlir.builtin import builtin
    return get_location_stack().peek_default(builtin.UnknownLoc())


def _print_location_epilogue(this, printer, opts):
    if opts.print_locations:
        printer.print_line(this.location.emit())


print_location = epilogue(_print_location_epilogue)


class MlirTypeMeta(DialectKind):
    def _register_(cls, dialect):
        dialect.register_type(cls)


class MlirType(metaclass=MlirTypeMeta):
    @abc.abstractmethod
    def emit(self) -> str:
        raise NotImplementedError()


@dataclasses.dataclass(frozen=True)
class MlirValue:
    type: MlirType
    raw_name: str
    location: MlirLocation = default_field(_default_location, init=False)

    @property
    def name(self) -> str:
        return f"%{self.raw_name}"


@dataclasses.dataclass(frozen=True)
class MlirSymbol:
    raw_name: str

    @property
    def name(self) -> str:
        return f"@{self.raw_name}"


@dataclasses.dataclass
class MlirBlock(WithId):
    operations: List['MlirOp'] = default_field(list, init=False)
    arguments: List[MlirValue] = default_field(list, init=False)
    # parent is of type MlirRegion.
    parent: OptionalWeakRef = default_field(constant(None), init=False)

    def add_operation(self, operation: 'MlirOp'):
        operation.set_parent(self)
        self.operations.append(operation)

    def set_parent(self, parent: 'MlirRegion'):
        self.parent = weakref.ref(parent)

    def print(self, printer: PrinterBase, opts: PrintOpts):
        for operation in self.operations:
            operation.print(printer, opts)


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
    blocks: List[MlirBlock] = default_field(list, init=False)
    # @parent is of type MlirOp.
    parent: OptionalWeakRef = default_field(constant(None), init=False)

    def new_block(self) -> MlirBlock:
        block = MlirBlock()
        block.set_parent(self)
        self.blocks.append(block)
        return block

    def set_parent(self, parent: 'MlirOp'):
        self.parent = weakref.ref(parent)

    def print(self, printer: PrinterBase, opts: PrintOpts):
        for block in self.blocks:
            block.print(printer, opts)


class MlirOpMeta(DialectKind):
    def _register_(cls, dialect):
        dialect.register_op(cls)

    def __call__(cls, *args, **kwargs):
        obj = super().__call__(*args, **kwargs)
        try:
            block = get_block_stack().peek()
        except IndexError:
            pass
        else:
            block.add_operation(obj)
        return obj


@dataclasses.dataclass
class MlirOp(WithId, metaclass=MlirOpMeta):
    regions: List[MlirRegion] = default_field(list, init=False)
    operands: List[MlirValue] = default_field(list, init=False)
    results: List[MlirValue] = default_field(list, init=False)
    attr_dict: Mapping = default_field(dict, init=False)
    # @parent is of type MlirBlock.
    parent: OptionalWeakRef = default_field(constant(None), init=False)
    location: MlirLocation = default_field(_default_location, init=False)

    def new_region(self) -> MlirRegion:
        region = MlirRegion()
        region.set_parent(self)
        self.regions.append(region)
        return region

    def set_parent(self, parent: MlirBlock):
        self.parent = weakref.ref(parent)

    @print_location
    def print(self, printer: PrinterBase, opts: PrintOpts):
        self.print_op(printer, opts)
        if not self.regions:
            printer.flush()
            return
        printer.print(" {")
        printer.flush()
        printer.push()
        for region in self.regions:
            region.print(printer, opts)
        printer.pop()
        printer.print_line("}")

    @abc.abstractmethod
    def print_op(self, printer: PrinterBase, opts: PrintOpts):
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

    def register_attribute(self, attr: type):
        self._register(attr, "attr", MlirAttribute)


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
