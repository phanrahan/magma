import abc
import contextlib
import dataclasses
import functools
import itertools
from typing import Any, Iterable, Optional, Set, Tuple, Union

from magma.debug import get_debug_info, debug_info as DebugInfo
from magma.ref import get_ref_inst


@functools.lru_cache(None)
def _bit_type():
    # NOTE(leonardt): Circular dependency.
    from magma.bit import Bit
    return Bit


@functools.lru_cache(None)
def _abstract_register_type():
    # NOTE(rsetaluri): Circular dependency.
    from magma.primitives.register import AbstractRegister
    return AbstractRegister


@functools.lru_cache(None)
def _enable_type():
    # NOTE(rsetaluri): Circular dependency.
    from magma.clock import Enable
    return Enable


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
        if self.root._default_drivers.pop(i, None) is not None:
            self.root.builder.remove_default_driver(i)

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
        if self.root is not self:
            raise RuntimeError("Can only get default drivers from root")
        return (
            ConditionalWire(k, v)
            for k, v in self._default_drivers.items()
        )

    def get_default_drivers_dict(self) -> Iterable[ConditionalWire]:
        if self.root is not self:
            raise RuntimeError("Can only get default drivers from root")
        return self._default_drivers

    def get_default_driver(self, drivee) -> Any:
        if self.root is not self:
            raise RuntimeError("Can only get default driver from root")
        return self._default_drivers[drivee]

    def add_default_driver(self, drivee, driver):
        if self.root is not self:
            raise RuntimeError("Can only add default driver to root")
        self._default_drivers[drivee] = driver
        self.root.builder.add_default_driver(drivee, driver)

    def children(self) -> Iterable['_BlockBase']:
        yield from self._children

    def __enter__(self):
        if self.condition is not None:
            self.root.builder.add_condition(self.condition)
        _set_curr_block(self)
        return self

    def _add_reg_enables(self):
        """
        If we wire the input of a register, check if there is an enable port
        and wire to 1 if found.

        This will overwrite an existing wiring if the user already has done it.

        The warning raised will indicate to the user that the explicit wiring
        is unnecessary and promote the idiom of not explicitly wiring enables.
        """
        conditional_wires = list(self._conditional_wires)
        # We need to keep track of Enable values we've wired and make sure to
        # only wire them once. Otherwise, an elaborated register input value may
        # be wired multiple times.
        # NOTE(leonardt): If we wanted to allow users to wire Enable values
        # explicitly, we could lookup whether a wire to enable exists in
        # conditional_wires (which would also avoid multiple wirings).
        seen = set()
        for wire in conditional_wires:
            inst = get_ref_inst(wire.drivee.name)
            if (
                    inst is None
                    or not isinstance(type(inst), _abstract_register_type())
            ):
                continue
            ce_port = type(inst).get_enable(inst)
            if (
                    ce_port is None
                    # Explicitly wired in this block, skip.
                    or self.get_conditional_wires_for_drivee(ce_port)
                    or (
                        ce_port.driven()
                        and not ce_port.driven_implicitly_by_when
                    )
                    or ce_port in seen
            ):
                continue
            ce_port.wire(1, driven_implicitly_by_when=True)
            seen.add(ce_port)

    @abc.abstractmethod
    def _get_exit_block(self):
        """Returns the block that should be set as the current block when
        __exit__ is called.
        """
        raise NotImplementedError()

    def __exit__(self, exc_type, exc_value, traceback):
        self._add_reg_enables()
        _set_curr_block(self._get_exit_block())
        _set_prev_block(self)


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
    # NOTE(leonardt): We can't use Bit here because of circular dependency, so
    # instead we enforce it in the public constructors (e.g. m.when).
    condition: Any


@dataclasses.dataclass
class _ElseWhenBlockInfo(_WhenBlockInfo):
    pass


class _WhenBlock(_BlockBase):
    def __init__(
            self,
            parent: Optional[_BlockBase],
            info: _WhenBlockInfo,
            debug_info: Optional[DebugInfo] = None,
    ):
        super().__init__(parent)
        self._info = info
        self._elsewhens = list()
        self._otherwise = None
        self._builder = None
        if self._parent is None:
            # NOTE(rsetaluri): Circular dependency.
            from magma.primitives.when import WhenBuilder
            self._builder = WhenBuilder(self)
            if debug_info is not None:
                self._builder.debug_info = debug_info

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

    def _get_exit_block(self):
        return self._parent


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

    def _get_exit_block(self):
        return self._parent._get_exit_block()


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

    def _get_exit_block(self):
        return self._parent._get_exit_block()


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
    if not isinstance(cond, _bit_type()):
        raise TypeError(f"Invalid when cond {cond}, should be Bit")
    info = _WhenBlockInfo(cond)
    curr_block = _get_curr_block()
    if curr_block is None:
        return _WhenBlock(None, info, get_debug_info(3))
    return curr_block.spawn(info)


def elsewhen(cond):
    if not isinstance(cond, _bit_type()):
        raise TypeError(f"Invalid elsewhen cond {cond}, should be Bit")
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
