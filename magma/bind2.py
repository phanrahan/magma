import dataclasses
from typing import Dict, List, Optional, Union

from magma.circuit import DefineCircuitKind, CircuitKind, CircuitType
from magma.compile_guard import get_active_compile_guard_info, CompileGuardInfo
from magma.generator import Generator2Kind, Generator2
from magma.passes.passes import DefinitionPass, pass_lambda
from magma.view import PortView
from magma.wire_utils import wire_value_or_port_view
from magma.t import Type, In


_BOUND_INSTANCE_INFO_KEY = "_bound_instance_info_"
_BOUND_GENERATOR_INFO_KEY = "_bound_generator_info_"
_IS_BOUND_MODULE_KEY = "_is_bound_module_"

DutType = Union[DefineCircuitKind, Generator2Kind]
BindModuleType = Union[CircuitKind, Generator2Kind]
ArgumentType = Union[Type, PortView]


@dataclasses.dataclass(frozen=True)
class BoundInstanceInfo:
    args: List[ArgumentType]
    compile_guards: List[CompileGuardInfo]


@dataclasses.dataclass(frozen=True)
class BoundGeneratorInfo:
    bind_generator: Generator2Kind
    compile_guards: List[CompileGuardInfo]


def set_bound_instance_info(inst: CircuitType, info: BoundInstanceInfo):
    global _BOUND_INSTANCE_INFO_KEY
    setattr(inst, _BOUND_INSTANCE_INFO_KEY, info)


def maybe_get_bound_instance_info(
        inst: CircuitType
) -> Optional[BoundInstanceInfo]:
    global _BOUND_INSTANCE_INFO_KEY
    return getattr(inst, _BOUND_INSTANCE_INFO_KEY, None)


def is_bound_instance(inst: CircuitType) -> bool:
    return maybe_get_bound_instance_info(inst) is not None


def set_is_bound_module(defn: CircuitKind, value: bool = True):
    global _IS_BOUND_MODULE_KEY
    setattr(defn, _IS_BOUND_MODULE_KEY, value)


def is_bound_module(defn: CircuitKind) -> bool:
    global _IS_BOUND_MODULE_KEY
    return getattr(defn, _IS_BOUND_MODULE_KEY, False)


def get_bound_generator_infos(inst: CircuitType) -> List[BoundGeneratorInfo]:
    global _BOUND_GENERATOR_INFO_KEY
    try:
        info = getattr(inst, _BOUND_GENERATOR_INFO_KEY)
    except AttributeError:
        info = list()
        setattr(inst, _BOUND_GENERATOR_INFO_KEY, info)
    return info


class BindGenerators(DefinitionPass):
    def __call__(self, defn):
        if not isinstance(defn, Generator2):
            return
        gen = type(defn)
        for info in get_bound_generator_infos(type(defn)):
            bind_module = info.bind_generator(
                defn, *defn._args_, **defn._kwargs_
            )
            bind_args = getattr(bind_module, "bind2_args", list())
            _bind_impl(defn, bind_module, bind_args, info.compile_guards)


bind_generators = pass_lambda(BindGenerators)


def make_bind_ports(defn_or_decl: CircuitKind) -> Dict[str, Type]:
    return {
        name: In(type(port))
        for name, port in defn_or_decl.interface.ports.items()
    }


def _bind_generator_impl(
        dut: Generator2Kind,
        bind_generator: Generator2Kind,
        compile_guards: List[CompileGuardInfo],
):
    infos = get_bound_generator_infos(dut)
    info = BoundGeneratorInfo(bind_generator, compile_guards)
    infos.append(info)


def _bind_impl(
        dut: DefineCircuitKind,
        bind_module: CircuitKind,
        args: List[ArgumentType],
        compile_guards: List[CompileGuardInfo],
):
    arguments = list(dut.interface.ports.values()) + args
    with dut.open():
        inst = bind_module()
        for param, arg in zip(inst.interface.ports.values(), arguments):
            wire_value_or_port_view(param, arg)
        info = BoundInstanceInfo(args, compile_guards)
        set_bound_instance_info(inst, info)
        set_is_bound_module(bind_module, True)


def bind2(
        dut: DutType,
        bind_module: BindModuleType,
        *args,
):
    args = list(args)
    compile_guards = list(get_active_compile_guard_info())
    are_generators = (
        isinstance(dut, Generator2Kind) and
        isinstance(bind_module, Generator2Kind)
    )
    if are_generators:
        if args:
            raise ValueError(
                "Expected no arguments for binding generators. "
                "Implement bind_arguments() instead."
            )
        _bind_generator_impl(dut, bind_module, compile_guards)
        return
    are_modules = (
        isinstance(dut, DefineCircuitKind) and
        isinstance(dut, CircuitKind)
    )
    if are_modules:
        _bind_impl(dut, bind_module, args, compile_guards)
        return
    raise TypeError(dut, bind_module)
