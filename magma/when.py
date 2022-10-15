import abc
import contextlib
import dataclasses
import itertools
from typing import Any, Iterable, Optional, Set, Tuple, Union


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

    def get_conditional_wires_for_drivee(self, i):
        return list(
            filter(lambda x: x.drivee is i, self._conditional_wires)
        )

    def remove_conditional_wire(self, i):
        self._conditional_wires = list(
            filter(lambda x: x.drivee is not i, self._conditional_wires)
        )

    def add_conditional_wire(self, i, o):
        self._conditional_wires.append(ConditionalWire(i, o))
        builder = self.root.builder
        if i.driven() and i not in builder.output_to_index:
            driver = i.value()
            # Keep wired when contexts because in this case, the driver could
            # have been wired in a different when context (so the default value
            # comes from the result of a previous when context)
            i.unwire(driver, keep_wired_when_contexts=True)
            self.root.add_default_driver(i, driver)
        self.root.builder.add_drivee(i)
        self.root.builder.add_driver(o)

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
        self.root.builder.add_default_driver(drivee, driver)

    def children(self) -> Iterable['_BlockBase']:
        yield from self._children

    def __enter__(self):
        self.root.builder.add_condition(self.condition)
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
        self._builder = None
        if self._parent is None:
            from magma.primitives.when import WhenBuilder
            self._builder = WhenBuilder(self)

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
    def builder(self) -> Any:
        if self._builder is None:
            raise AttributeError()
        return self._builder

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
        return self._parent.new_elsewhen_block(info)

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


@contextlib.contextmanager
def no_when():
    block = _get_curr_block()
    _set_curr_block(None)
    yield
    _set_curr_block(block)


@contextlib.contextmanager
def temp_when(temp_ctx):
    block = _get_curr_block()
    _set_curr_block(temp_ctx)
    yield
    _set_curr_block(block)


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


def _get_else_block(block: _BlockBase) -> Optional[_BlockBase]:
    if isinstance(block, _OtherwiseBlock):
        return None
    if isinstance(block, _ElseWhenBlock):
        # TODO(rsetaluri): We could augment _ElseWhenBlock to keep track of its
        # index in the parent block, or alternatively keep an explicit pointer
        # to the next else/otherwise block in each _ElseWhenBlock.
        parent_elsewhen_blocks = list(block._parent.elsewhen_blocks())
        index = parent_elsewhen_blocks.index(block) + 1
        if index == len(parent_elsewhen_blocks):
            return block._parent.otherwise_block
        return parent_elsewhen_blocks[index]
    if isinstance(block, _WhenBlock):
        try:
            else_block = next(block.elsewhen_blocks())
        except StopIteration:
            pass
        else:
            return else_block
        return block.otherwise_block


_Op = Union[ConditionalWire, _BlockBase]


def _get_then_ops(block: _BlockBase) -> Iterable[_Op]:
    yield from block.conditional_wires()
    yield from block.children()


def _get_else_ops(block: _BlockBase) -> Iterable[_Op]:
    if isinstance(block, _OtherwiseBlock):
        return _get_then_ops(block)
    if isinstance(block, _ElseWhenBlock):
        return (block,)
    raise TypeError(block)


def _get_assignees_and_latches(ops: Iterable[_Op]) -> Tuple[Set, Set]:
    """Compute the assigned values and latches implied by a block.

    Note: this is a conservative check that requires values are assigned in
    every case.  For example, there may be an unreachable case where a value is
    not assigned, but that requires symbolic evaluation to discover.  In
    general, symbolic evaluation is difficult, but may be viable in the
    hardware domain where we may have less issues with path explosion,
    aliasing, arrays, etc...

    Parameters
    ----------
    ops : Iterable[_Op]
        A sequence of ops (assignment or if-then-else block)

    Returns
    -------
    Set[Type]
        The values assigned in this block by any operation.

    Set[Type]
        The latches implied by this block, i.e. values which are not assigned in
        all branches.
    """
    assignees, latches = set(), set()
    for op in ops:
        if isinstance(op, ConditionalWire):
            assignees.add(op.drivee)
            continue
        if isinstance(op, _BlockBase):
            then_ops = _get_then_ops(op)
            then_assignees, then_latches = _get_assignees_and_latches(
                then_ops
            )
            else_block = _get_else_block(op)
            if else_block is None:
                latches.update(then_latches.difference(assignees))
                latches.update(then_assignees.difference(assignees))
                continue
            else_ops = _get_else_ops(else_block)
            else_assignees, else_latches = _get_assignees_and_latches(
                else_ops
            )
            latches.update(then_latches.difference(assignees))
            latches.update(else_latches.difference(assignees))
            latches.update(
                (
                    then_assignees
                    .symmetric_difference(else_assignees)
                    .difference(assignees)
                )
            )
            assignees.update(then_assignees.union(else_assignees))
            # Filter out any latches that were created in this when context.
            latches = set(filter(
                lambda x: x.enclosing_when_context is not op,
                latches
            ))
            continue
        raise TypeError(op)
    return assignees, latches


def find_inferred_latches(block: _BlockBase) -> Set:
    if not (isinstance(block, _WhenBlock) and block.root is block):
        raise TypeError("Can only find inferred latches on root when block")
    ops = tuple(block.default_drivers()) + (block,)
    _, latches = _get_assignees_and_latches(ops)
    return latches


def when(cond):
    info = _WhenBlockInfo(cond)
    curr_block = _get_curr_block()
    if curr_block is None:
        return _WhenBlock(None, info)
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
