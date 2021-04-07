import ast
import libcst as cst
import libcst.matchers as match
import magma as magma_module
from typing import Optional, MutableMapping, Sequence

from ast_tools.stack import SymbolTable
from ast_tools.passes import (PASS_ARGS_T, Pass, apply_passes, ssa,
                              if_to_phi, bool_to_bit)
from ast_tools.common import gen_free_name, to_module

from ..circuit import Circuit, IO
from ..clock import AbstractReset
from ..clock_io import ClockIO, gen_clock_io
from ..t import Type, Direction
from ..protocol_type import MagmaProtocol, MagmaProtocolMeta
from ..primitives.register import Register

from .util import build_io_args, build_call_args, wire_call_result


class _SequentialListWrapper(list):
    def __getitem__(self, i):
        result = super().__getitem__(i)
        if isinstance(type(result), Register):
            # Patch in prev method as syntax sugar for previous value
            result.prev = lambda: result.O
        if isinstance(result, list):
            return _SequentialListWrapper(result)
        return result

    def __setitem__(self, i, value):
        item = self[i]
        if not isinstance(item, Circuit):
            raise TypeError("Excepted setitem target to be a Circuit")

        if not isinstance(value, (Circuit, int, Type)):
            raise TypeError("Excepted setitem value to be a Circuit, Type, or "
                            f"int, not {type(value)}")

        item(value)


class _SequentialRegisterWrapperMeta(MagmaProtocolMeta):
    _cache = {}

    def _to_magma_(cls):
        return cls.T

    def _qualify_magma_(cls, direction: Direction):
        return cls[cls.T.qualify(direction)]

    def _flip_magma_(cls):
        return cls[cls.T.flip()]

    def _from_magma_value_(cls, val: Type):
        return val

    def _is_oriented_magma_(cls, direction):
        return cls.T.is_oriented(direction)

    def __getitem__(cls, T):
        if T not in cls._cache:
            cls._cache[T] = type(cls)(f"_SequentialRegisterWrapper{T}",
                                      (cls, ), {"T": T})
        return cls._cache[T]

    def __eq__(cls, rhs):
        if not isinstance(rhs, _SequentialRegisterWrapperMeta):
            return NotImplemented
        return cls.T is rhs.T

    def __hash__(cls):
        return hash(cls.T)

    def __repr__(cls):
        return f"_SequentialRegisterWrapper{cls.T}"

    def flat_length(cls):
        return cls.T.flat_length()

    def unflatten(cls, value):
        return cls.T.unflatten(value)

    @property
    def direction(cls) -> int:
        return cls.T.direction


class _SequentialRegisterWrapper(MagmaProtocol,
                                 metaclass=_SequentialRegisterWrapperMeta):
    """
    Wraps sequential attributes to implement register getattr syntax and
    general circuit call syntax, e.g.

        def __init__(self):
            self.x = Register(4)

        def __call__(self, ...) -> ...:
            if S:
                return self.x(I)  # call syntax
            return self.x + 1     # attribute syntax
    """

    def __init__(self, circuit: Circuit):
        assert isinstance(circuit, Circuit)
        self.circuit = circuit

    def _get_magma_value_(self):
        # Return output
        return self.circuit()

    # TODO: Clever way to pass through operators to the underlying value?
    def __add__(self, other):
        return self._get_magma_value_() + other

    def __radd__(self, other):
        return other + self._get_magma_value_()

    def __sub__(self, other):
        return self._get_magma_value_() - other

    def __rsub__(self, other):
        return other - self._get_magma_value_()

    def __mul__(self, other):
        return self._get_magma_value_() * other

    def __rmul__(self, other):
        return other * self._get_magma_value_()

    def __truediv__(self, other):
        return self._get_magma_value_() / other

    def __rtruediv__(self, other):
        return other / self._get_magma_value_()

    def __floordiv__(self, other):
        return self._get_magma_value_() // other

    def __rfloordiv__(self, other):
        return other // self._get_magma_value_()

    def __mod__(self, other):
        return self._get_magma_value_() % other

    def __rmod__(self, other):
        return other % self._get_magma_value_()

    def __or__(self, other):
        return self._get_magma_value_() | other

    def __ror__(self, other):
        return other | self._get_magma_value_()

    def __xor__(self, other):
        return self._get_magma_value_() ^ other

    def __rxor__(self, other):
        return other ^ self._get_magma_value_()

    def __and__(self, other):
        return self._get_magma_value_() & other

    def __rand__(self, other):
        return other & self._get_magma_value_()

    def __eq__(self, other):
        return self._get_magma_value_() == other

    def __ne__(self, other):
        return self._get_magma_value_() != other

    def __ge__(self, other):
        return self._get_magma_value_() >= other

    def __gt__(self, other):
        return self._get_magma_value_() > other

    def __le__(self, other):
        return self._get_magma_value_() <= other

    def __lt__(self, other):
        return self._get_magma_value_() < other

    def __lshift__(self, other):
        return self._get_magma_value_() << other

    def __rlshift__(self, other):
        return other << self._get_magma_value_()

    def __rshift__(self, other):
        return self._get_magma_value_() >> other

    def __rrshift__(self, other):
        return other >> self._get_magma_value_()

    def __neg__(self):
        return -self._get_magma_value_()

    def __invert__(self):
        return ~self._get_magma_value_()

    def ite(self, s, t, f):
        return self._get_magma_value_().ite(s, t, f)

    def __call__(self, *args, **kwargs):
        return self.circuit(*args, **kwargs)

    def __getitem__(self, i):
        key = i._get_magma_value_() if isinstance(i, MagmaProtocol) else i
        return self._get_magma_value_()[key]

    def __getattr__(self, key):
        return self._get_magma_value_()[key]

    def __len__(self):
        return len(self._get_magma_value_())

    @property
    def debug_name(self):
        return self._get_magma_value_().debug_name


def sequential_getattribute(self, key):
    """
    Wrap lists so we can use the setattr interface with lists of registers
    """
    result = object.__getattribute__(self, key)
    if isinstance(result, list):
        return _SequentialListWrapper(result)
    if isinstance(type(result), Register):
        return _SequentialRegisterWrapper[type(result())](result)
    return result


def sequential_setattr(self, key, value):
    # TODO: for now we assume this is a register, ideally we'd type check this,
    # but we need to have a notion of a register primitive (e.g. right now the
    # mantle reg wraps the coreir reg primitive, so technically the register is
    # an arbitrary user-defined circuit)

    target = object.__getattribute__(self, key)
    # We can at least match the value is a circuit with outputs that match the
    # input of the attribute circuit
    if not isinstance(target, Circuit):
        raise TypeError("Excepted setattr key to be a Circuit")

    if isinstance(value, MagmaProtocol):
        value = value._get_magma_value_()
    if not isinstance(value, (Circuit, int, Type)):
        raise TypeError("Excepted setattr value to be a Circuit, Type, or int",
                        f"not {type(value)}")

    # Simply use function call syntax for now (should automatically retrieve
    # the output of value)
    target(value)


def _process_phi_arg(arg):
    if isinstance(arg, Circuit):
        # Call with no args to retrieve output(s)
        arg = arg()
        if isinstance(arg, list):
            # TODO: We could support tuples/products
            raise TypeError("Cannot use circuit with multiple outputs as "
                            "argument to phi")
    return arg


def _seq_phi(s, t, f):
    if isinstance(t, tuple):
        assert isinstance(f, tuple)
        return tuple(_seq_phi(s, _t, _f) for _t, _f in zip(t, f))
    # Unpack registers/circuits used in getattr syntax
    t, f = map(_process_phi_arg, (t, f))
    return s.ite(t, f)


class _RegisterUpdater(cst.CSTTransformer):
    """Update m.Register params implicitly"""
    def __init__(self, env, reset_type, has_enable, reset_priority, magma_id):
        self.env = env

        self.reset_type = cst.Arg(
            cst.parse_expression(f"{magma_id}.{reset_type}"),
            cst.Name("reset_type"),
        )
        self.has_enable = cst.Arg(
            cst.Name(str(has_enable)),
            cst.Name("has_enable"),
        )
        self.reset_priority = cst.Arg(
            cst.Name(str(reset_priority)),
            cst.Name("reset_priority"),
        )

    def _is_m_register(self, node):
        return (
            match.matches(
                node.func,
                match.Attribute(match.DoNotCare(), match.Name("Register"))
            ) and
            eval(node.func.value.value, {}, self.env) is magma_module
        )

    def leave_Call(self, original_node, updated_node):
        # find m.Register
        if self._is_m_register(updated_node):
            args = []
            keywords = set()
            for arg in updated_node.args:
                args.append(arg)
                if arg.keyword:
                    keywords.add(arg.keyword.value)
            if "reset_type" not in keywords:
                args.append(self.reset_type)
            if "has_enable" not in keywords:
                args.append(self.has_enable)
            if "reset_priority" not in keywords:
                args.append(self.reset_priority)

            return updated_node.with_changes(args=args)

        return updated_node


class _UpdateRegister(Pass):
    """Update m.Register params implicitly"""
    def __init__(self, reset_type, has_enable, reset_priority):
        self.reset_type = reset_type
        self.has_enable = has_enable
        self.reset_priority = reset_priority

    def _get_or_add_magma_module(self, tree: ast.AST, env: SymbolTable):
        magma_id = None
        for k, v in env.items():
            if v is magma_module:
                magma_id = k
                break
        if magma_id is None:
            magma_id = gen_free_name(tree, env)
            env.locals[magma_id] = magma_module
        return env, magma_id

    def rewrite(
        self, tree: ast.AST, env: SymbolTable, metadata: MutableMapping
    ) -> PASS_ARGS_T:

        env, magma_id = self._get_or_add_magma_module(tree, env)
        updater = _RegisterUpdater(env, self.reset_type,
                                   self.has_enable, self.reset_priority,
                                   magma_id)
        return tree.visit(updater), env, metadata


class _PrevReplacer(cst.CSTTransformer):
    """Replace self.attr.prev() with __magma_sequential2_attr"""
    def __init__(self):
        super().__init__()
        self.attrs = {}

    def leave_Call(self, original_node, updated_node):
        # find self.attr.prev()
        if match.matches(
            updated_node.func,
            match.Attribute(
                match.Attribute(match.Name("self")),
                match.Name("prev")
            )
        ):
            # replace self.attr.prev() with __magma_sequential2_attr
            attr = updated_node.func.value
            var = f"__magma_sequential2_{attr.attr.value}"
            self.attrs[var] = attr
            return cst.Name(var)
        return updated_node
        return self.generic_visit(node)


class _ReplacePrev(Pass):
    """
    Replace all self.attr.prev() usage

    def __call__(self):
        return self.attr.prev()

    def __call__(self):
        __magma_sequential2_attr = self.attr
        return __magma_sequential2_attr
    """

    def rewrite(self,
                tree: ast.AST,
                env: SymbolTable,
                metadata: MutableMapping) -> PASS_ARGS_T:
        prev_replacer = _PrevReplacer()
        tree = tree.visit(prev_replacer)

        assigns = []
        for var, attr in prev_replacer.attrs.items():
            assigns.append(cst.SimpleStatementLine([cst.Assign(targets=[
                cst.AssignTarget(cst.Name(var))
            ], value=attr)]))
        new_body = tuple(assigns) + tree.body.body
        tree = tree.with_changes(body=tree.body.with_changes(body=new_body))

        return tree, env, metadata


def sequential2(pre_passes=[], post_passes=[],
                debug: bool = False,
                env: Optional[SymbolTable] = None,
                path: Optional[str] = None,
                file_name: Optional[str] = None,
                annotations: Optional[dict] = None,
                reset_type: AbstractReset = None,
                has_enable: bool = False,
                reset_priority: bool = True,
                output_port_names: Optional[Sequence[str]] = None,
                ):
    passes = (pre_passes + [
        _ReplacePrev(), ssa(strict=False), bool_to_bit(), if_to_phi(_seq_phi)
    ] + post_passes)

    clock_io = gen_clock_io(reset_type, has_enable)

    def seq_inner(cls):
        if reset_type:
            update_register = _UpdateRegister(reset_type,
                                              has_enable, reset_priority)
            if cls.__init__ is not object.__init__:
                cls.__init__ = apply_passes(
                    passes=[update_register], debug=debug, env=env, path=path,
                    file_name=file_name
                )(cls.__init__)

        cls.__call__ = apply_passes(passes, debug=debug, env=env,
                                    path=path,
                                    file_name=file_name)(cls.__call__)
        if annotations is None:
            _annotations = cls.__call__.__annotations__
        else:
            _annotations = annotations

        if "self" in _annotations:
            raise Exception("Assumed self did not have annotation")

        io_args = build_io_args(_annotations, output_port_names)

        class SequentialCircuit(Circuit):
            name = cls.__name__
            io = IO(**io_args) + clock_io
            call_args = [cls()]

            # Monkey patch setattribute for register assign syntax, we could
            # also add this in a Sequential base class, but if we do that we
            # might as well use a metaclass rather than a decorator, but to
            # preserve the old interface we do this for now
            cls.__setattr__ = sequential_setattr

            # also need to patch getattr to support list attributes (see
            # test_sequential2:test_sequential2_pre_unroll)
            cls.__getattribute__ = sequential_getattribute

            call_args += build_call_args(io, _annotations)

            call_result = cls.__call__(*call_args)
            wire_call_result(
                io,
                call_result,
                cls.__call__.__annotations__,
                output_port_names
            )
        return SequentialCircuit
    return seq_inner
