from typing import Union

from magma.circuit import DefineCircuitKind, CircuitKind
from magma.generator import Generator2Kind, Generator2
from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.xmr import XMRSink, XMRSource
from magma.view import PortView


_BOUND_INSTANCE_INFO_KEY = "_bound_instance_info_"
_BOUND_GENERATOR_INFO_KEY = "_bound_generator_info_"

DutType = Union[DefineCircuitKind, Generator2Kind]
BindModuleType = Union[CircuitKind, Generator2Kind]


def _wire_value_or_driver(param, arg):
    assert param.is_input()
    if arg.is_output():
        param @= arg
    elif arg.is_input():
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


def get_bound_instance_info(inst):
    return getattr(inst, _BOUND_INSTANCE_INFO_KEY, None)


def is_bound_instance(inst) -> bool:
    return get_bound_instance_info(inst) is not None


def get_bound_generator_info(inst):
    return getattr(inst, _BOUND_GENERATOR_INFO_KEY, None)


def is_bound_generator(inst) -> bool:
    return get_bound_generator_info(inst) is not None


class BindGenerators(DefinitionPass):
    def __call__(self, defn):
        if not isinstance(defn, Generator2):
            return
        gen = type(defn)
        bind_generators = get_bound_generator_info(gen) or list()
        for bind_generator in bind_generators:
            bind_module = bind_generator(*defn._args_, **defn._kwargs_)
            bind2(defn, bind_module, *bind_module.bind2_arguments(defn))


bind_generators = pass_lambda(BindGenerators)


def bind2_generator(dut: Generator2Kind, bind_module: Generator2Kind):
    try:
        info = getattr(dut, _BOUND_GENERATOR_INFO_KEY)
    except AttributeError:
        info = list()
        setattr(dut, _BOUND_GENERATOR_INFO_KEY, info)
    info.append(bind_module)


def bind2(
        dut: DefineCircuitKind,
        bind_module: CircuitKind,
        *args,
        compile_guard=None):
    arguments = list(dut.interface.ports.values()) + list(args)
    with dut.open():
        inst = bind_module()
        for param, arg in zip(inst.interface.ports.values(), arguments):
            _wire_bind_arg(param, arg)
        info = {"args": args, "compile_guard": compile_guard}
        setattr(inst, _BOUND_INSTANCE_INFO_KEY, info)
