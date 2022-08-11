import abc
import contextlib
import dataclasses
import itertools
from typing import Any, Iterable, List, Optional, Tuple


class WhenSyntaxError(SyntaxError):
    pass


class NoPrecedingWhenError(WhenSyntaxError):
    def __init__(self, type):
        super().__init__(f"Cannot use {type} without a previous when")


class ElsewhenWithoutPrecedingWhenError(NoPrecedingWhenError):
    def __init__(self):
        super().__init__("elsewhen")


class OtherwiseWithoutPrecedingWhenError(NoPrecedingWhenError):
    def __init__(self):
        super().__init__("otherwise")


@dataclasses.dataclass(frozen=True)
class ConditionalWire:
    drivee: Any
    driver: Any


class _BlockBase(contextlib.AbstractContextManager):
    def __init__(self, parent: Optional['_WhenBlock']):
        self._parent = parent
        self._children = list()
        self._conditional_wires = list()
        self._default_drivers = dict()

    def spawn(self, info: '_WhenBlockInfo') -> '_WhenBlock':
        child = _WhenBlock(self, info)
        self._children.append(child)
        return child

    def add_conditional_wire(self, i, o):
        self._conditional_wires.append(ConditionalWire(i, o))
        if i.driven():
            driver = i.value()
            i.unwire(driver)
            self.root.add_default_driver(i, driver)

    @property
    @abc.abstractmethod
    def root(self) -> '_WhenBlock':
        raise NotImplementedError()

    @abc.abstractmethod
    def new_elsewhen_block(self, info: '_ElseWhenBlockInfo'):
        raise NotImplementedError()

    @abc.abstractmethod
    def new_otherwise_block(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def condition(self) -> Optional:
        raise NotImplementedError()

    @abc.abstractmethod
    def elsewhen_blocks(self) -> Iterable['_BlockBase']:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def otherwise_block(self) -> Optional['_BlockBase']:
        raise NotImplementedError()

    def conditional_wires(self) -> Iterable[ConditionalWire]:
        yield from self._conditional_wires

    def default_drivers(self) -> Iterable[ConditionalWire]:
        return (
            ConditionalWire(k, v)
            for k, v in self._default_drivers.items()
        )

    def get_default_driver(self, drivee) -> Any:
        return self._default_drivers[drivee]

    def add_default_driver(self, drivee, driver):
        if self.root is not self:
            raise RuntimeError("Can only add default driver to root")
        self._default_drivers[drivee] = driver

    def children(self) -> Iterable['_BlockBase']:
        yield from self._children

    def __enter__(self):
        _set_curr_block(self)
        return self


BlockBase = _BlockBase


def get_all_blocks(
        block: _BlockBase,
        include_self: bool = True,
) -> Iterable[_BlockBase]:
    if include_self:
        yield block
    sub_blocks = itertools.chain(
        block.children(),
        block.elsewhen_blocks(),
        () if block.otherwise_block is None else (block.otherwise_block,),
    )
    for sub_block in sub_blocks:
        yield from get_all_blocks(sub_block)


@dataclasses.dataclass
class _WhenBlockInfo:
    condition: Any  # TODO(rsetaluri): Should actually be bit


@dataclasses.dataclass
class _ElseWhenBlockInfo(_WhenBlockInfo):
    pass


class _WhenBlock(_BlockBase):
    def __init__(self, parent: Optional[_BlockBase], info: _WhenBlockInfo):
        super().__init__(parent)
        self._info = info
        self._elsewhens = list()
        self._otherwise = None

    def new_elsewhen_block(self, info: '_ElseWhenBlockInfo'):
        block = _ElseWhenBlock(self, info)
        self._elsewhens.append(block)
        return block

    def new_otherwise_block(self):
        if self._otherwise is not None:
            raise WhenSyntaxError()
        block = _OtherwiseBlock(self)
        self._otherwise = block
        return block

    @property
    def root(self) -> '_WhenBlock':
        if self._parent is None:
            return self
        return self._parent.root

    @property
    def condition(self) -> Any:
        return self._info.condition

    def elsewhen_blocks(self) -> Iterable['_BlockBase']:
        yield from self._elsewhens

    @property
    def otherwise_block(self) -> Optional['_BlockBase']:
        return self._otherwise

    def __enter__(self):
        this = _BlockBase.__enter__(self)
        assert this is self
        _set_prev_block(None)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        _set_curr_block(self._parent)
        _set_prev_block(self)


class _ElseWhenBlock(_BlockBase):
    def __init__(self, parent: Optional[_BlockBase], info: _ElseWhenBlockInfo):
        super().__init__(parent)
        self._info = info

    def new_elsewhen_block(self, info: '_ElseWhenBlockInfo'):
        return self._parent.new_elsewhen_block()

    def new_otherwise_block(self):
        return self._parent.new_otherwise_block()

    @property
    def root(self) -> _WhenBlock:
        return self._parent.root

    @property
    def condition(self) -> Any:
        return self._info.condition

    def elsewhen_blocks(self) -> Iterable['_BlockBase']:
        yield from ()

    @property
    def otherwise_block(self) -> None:
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        _set_curr_block(self._parent._parent)
        _set_prev_block(self)


class _OtherwiseBlock(_BlockBase):
    def new_elsewhen_block(self, _):
        raise ElsewhenWithoutPrecedingWhenError()

    def new_otherwise_block(self):
        raise OtherwiseWithoutPrecedingWhenError()

    @property
    def root(self) -> _WhenBlock:
        return self._parent.root

    @property
    def condition(self) -> None:
        return None

    def elsewhen_blocks(self) -> Iterable['_BlockBase']:
        yield from ()

    @property
    def otherwise_block(self) -> None:
        return None

    def __exit__(self, exc_type, exc_value, traceback):
        _set_curr_block(self._parent._parent)
        _set_prev_block(self)


_curr_block = None
_prev_block = None


def _get_curr_block() -> Optional[_BlockBase]:
    global _curr_block
    return _curr_block


def _set_curr_block(curr_block: Optional[_BlockBase]):
    global _curr_block
    _curr_block = curr_block


def _reset_curr_block():
    _set_curr_block(None)


def _get_prev_block() -> Optional[_BlockBase]:
    global _prev_block
    return _prev_block


def _set_prev_block(prev_block: Optional[_BlockBase]):
    global _prev_block
    _prev_block = prev_block


def _reset_prev_block():
    _set_prev_block(None)


get_curr_block = _get_curr_block


def _reset_context():
    _reset_curr_block()
    _reset_prev_block()


reset_context = _reset_context


def when(cond):
    # TODO(rsetaluri): Figure out circular import.
    from magma.definition_context import get_definition_context
    info = _WhenBlockInfo(cond)
    curr_block = _get_curr_block()
    if curr_block is None:
        block = _WhenBlock(None, info)
        get_definition_context().get_child("when").add_open_block(block)
        return block
    return curr_block.spawn(info)


def elsewhen(cond):
    info = _ElseWhenBlockInfo(cond)
    prev_block = _get_prev_block()
    if prev_block is None:
        raise ElsewhenWithoutPrecedingWhenError()
    return prev_block.new_elsewhen_block(info)


def otherwise():
    prev_block = _get_prev_block()
    if prev_block is None:
        raise OtherwiseWithoutPrecedingWhenError()
    return prev_block.new_otherwise_block()


def finalize(block: _WhenBlock):
    # TODO(rsetaluri): Figure out circular import.
    from magma.primitives.when import When
    defn = When(block)
    inst = defn()
    defn.wire_instance(inst)
