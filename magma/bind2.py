from typing import Dict, List, Optional, Union

from magma.circuit import DefineCircuitKind, CircuitKind, CircuitType
from magma.generator import Generator2Kind, Generator2
from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.xmr import XMRSink, XMRSource
from magma.view import PortView
from magma.t import Type, In


_BOUND_INSTANCE_INFO_KEY = "_bound_instance_info_"
_BOUND_GENERATOR_INFO_KEY = "_bound_generator_info_"

DutType = Union[DefineCircuitKind, Generator2Kind]
BindModuleType = Union[CircuitKind, Generator2Kind]
ArgumentType = Union[Type, PortView]


def _wire_value_or_driver(param, arg):
    assert param.is_input()
    if arg.is_input():
        param @= arg.value()
    elif arg.is_mixed():
        for param_i, arg_i in zip(param, arg):
            _wire_value_or_driver(param_i, arg_i)
    else:
        param @= arg


def _wire_bind_arg(param, arg):
    if isinstance(arg, PortView):
        defn = arg.parent.inst.defn
        with defn.open():
            xmr_sink = XMRSink(arg)()
            _wire_value_or_driver(xmr_sink.I, arg.port)
        xmr_source = XMRSource(arg)()
        _wire_value_or_driver(param, xmr_source.O)
        return
    _wire_value_or_driver(param, arg)


def set_bound_instance_info(inst: CircuitType, info: Dict):
    setattr(inst, _BOUND_INSTANCE_INFO_KEY, info)


def get_bound_instance_info(inst: CircuitType) -> Dict:
    return getattr(inst, _BOUND_INSTANCE_INFO_KEY, None)


def is_bound_instance(inst: CircuitType) -> bool:
    return get_bound_instance_info(inst) is not None


def get_bound_generator_info(inst: CircuitType) -> List[Generator2Kind]:
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
        for bind_generator in get_bound_generator_info(gen):
            bind_module = bind_generator(defn, *defn._args_, **defn._kwargs_)
            bind_args = getattr(bind_module, "bind2_args", list())
            bind2(defn, bind_module, *bind_args)


bind_generators = pass_lambda(BindGenerators)


def make_bind_ports(defn_or_decl: CircuitKind) -> Dict[str, Type]:
    return {
        name: In(type(port))
        for name, port in defn_or_decl.interface.ports.items()
    }


def _bind_generator_impl(dut: Generator2Kind, bind_module: Generator2Kind):
    info = get_bound_generator_info(dut)
    info.append(bind_module)


def _bind_impl(
        dut: DefineCircuitKind,
        bind_module: CircuitKind,
        args: List[ArgumentType],
        compile_guard: str,
):
    arguments = list(dut.interface.ports.values()) + args
    with dut.open():
        inst = bind_module()
        for param, arg in zip(inst.interface.ports.values(), arguments):
            _wire_bind_arg(param, arg)
        info = {"args": args, "compile_guard": compile_guard}
        set_bound_instance_info(inst, info)


def bind2(
        dut: DutType,
        bind_module: BindModuleType,
        *args,
        compile_guard: Optional[str] = None,
):
    args = list(args)
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
        return _bind_generator_impl(dut, bind_module)
    are_modules = (
        isinstance(dut, DefineCircuitKind) and
        isinstance(dut, CircuitKind)
    )
    if are_modules:
        return _bind_impl(dut, bind_module, args, compile_guard)
    raise TypeError(dut, bind_module)
