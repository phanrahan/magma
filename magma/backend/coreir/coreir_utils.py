from collections import OrderedDict
import json
from hwtypes import BitVector
from magma.array import Array
from magma.bit import Digital
from magma.clock import Clock, AsyncReset, AsyncResetN, ClockTypes
from magma.ref import (ArrayRef, DefnRef, TupleRef, InstRef, NamedRef,
                       PortViewRef)
from magma.tuple import Tuple
from magma.protocol_type import magma_type, magma_value
from magma.backend.util import make_relative
from magma.t import Kind


class CoreIRBackendError(RuntimeError):
    pass


def _tuple_key_to_string(k):
    try:
        int(k)
        return f"_{k}"
    except ValueError:
        pass
    return k


def magma_name_to_coreir_select(name):
    if isinstance(name, InstRef):
        return f"{name.inst.name}.{name.name}"
    if isinstance(name, DefnRef):
        return f"self.{name.name}"
    if isinstance(name, ArrayRef):
        array_name = magma_name_to_coreir_select(name.array.name)
        if isinstance(name.index, int):
            idx_str = name.index
        else:
            assert isinstance(name.index, slice)
            idx_str = f"{name.index.start}:{name.index.stop}"
        return f"{array_name}.{idx_str}"
    if isinstance(name, TupleRef):
        tuple_name = magma_name_to_coreir_select(name.tuple.name)
        key_name = _tuple_key_to_string(name.index)
        return f"{tuple_name}.{key_name}"
    if isinstance(name, PortViewRef):
        # get select in its container definition
        inner_select = magma_name_to_coreir_select(name.view.port.name)
        return name.view.get_hierarchical_coreir_select() + inner_select
    raise NotImplementedError((name, type(name)))


def magma_port_to_coreir_port(port):
    if isinstance(port, Slice):
        return port.get_coreir_select()
    return magma_name_to_coreir_select(port.name)


def check_magma_type(type_, error_msg=""):
    type_ = magma_type(type_)
    if issubclass(type_, Array):
        msg = error_msg.format("Array({}, {})").format(str(type_.N), "{}")
        check_magma_type(type_.T, msg)
        return
    if issubclass(type_, Tuple):
        for (k, t) in zip(type_.keys(), type_.types()):
            msg = error_msg.format("Tuple({}:{})".format(k, "{}"))
            check_magma_type(t, msg)
        return
    if issubclass(type_, Digital):
        return
    raise CoreIRBackendError(error_msg.format(str(type_)))


def check_magma_interface(interface):
    # For now only allow Bit, Array, or Tuple.
    for name, port in interface.ports.items():
        check_magma_type(
            type(port), f"{name}: {type(port)} not supported by CoreIR backend"
        )


def magma_type_to_coreir_type(context, type_):
    type_ = magma_type(type_)

    if issubclass(type_, Array):
        return context.Array(type_.N,
                             magma_type_to_coreir_type(context, type_.T))
    if issubclass(type_, Tuple):
        zipped = zip(type_.keys(), type_.types())
        return context.Record({
            _tuple_key_to_string(k): magma_type_to_coreir_type(context, t)
            for (k, t) in zipped
        })
    if type_.is_input():
        if issubclass(type_, Clock):
            return context.named_types[("coreir", "clk")]
        if issubclass(type_, (AsyncReset, AsyncResetN)):
            return context.named_types[("coreir", "arst")]
        return context.Bit()
    if type_.is_output():
        if issubclass(type_, Clock):
            return context.named_types[("coreir", "clkIn")]
        if issubclass(type_, (AsyncReset, AsyncResetN)):
            return context.named_types[("coreir", "arstIn")]
        return context.BitIn()
    return context.BitInOut()


def magma_interface_to_coreir_module_type(context, interface):
    args = OrderedDict()
    for name, port in interface.ports.items():
        args[name] = magma_type_to_coreir_type(context, type(port))
    return context.Record(args)


def python_to_coreir_param_type(context, typ):
    if typ is int:
        return context.Int()
    if typ is bool:
        return context.Bool()
    if typ is str:
        return context.String()
    if typ is BitVector:
        return context.BitVector()
    raise NotImplementedError(typ)


def make_cparams(context, params):
    cparams = {
        k: python_to_coreir_param_type(context, t)
        for k, t in params.items()
    }
    return context.newParams(cparams)


def attach_debug_info(coreir_obj, debug_info, a=None, b=None):
    def fn(k, v):
        if a and b:
            return coreir_obj.add_metadata(a, b, k, v)
        return coreir_obj.add_metadata(k, v)

    fn("filename", json.dumps(make_relative(debug_info.filename)))
    fn("lineno", json.dumps(str(debug_info.lineno)))


def map_genarg(context, value):
    if isinstance(value, type) and issubclass(value, Clock):
        if value.is_input():
            return context.named_types[("coreir", "clkIn")]
        return context.named_types[("coreir", "clk")]
    if isinstance(value, type) and issubclass(value, (AsyncReset, AsyncResetN)):
        if value.is_input():
            return context.named_types[("coreir", "arstIn")]
        return context.named_types[("coreir", "arst")]
    return value


def get_module_of_inst(context, inst, lib):
    wrapped = getattr(inst, "wrappedModule", None)
    if wrapped and wrapped.context is context:
        return wrapped
    return lib.modules[type(inst).coreir_name]


def get_inst_args(inst):
    args = {}
    for name, value in inst.kwargs.items():
        if name == "name" or name == "loc":
            continue
        if isinstance(value, tuple):
            args[name] = BitVector[value[1]](value[0])
        else:
            args[name] = value
    return args


def constant_to_value(constant):
    assert constant.const()
    if isinstance(constant, Digital):
        return int(constant)
    if isinstance(constant, Array):
        values = [constant_to_value(c) for c in constant]
        return BitVector[len(constant)](values)
    raise NotImplementedError(constant)


class Slice:
    def __init__(self, value, low, high):
        self.value = value
        self.low = low
        self.high = high

    def get_coreir_select(self,):
        return (magma_name_to_coreir_select(self.value.name) +
                f".{self.low}:{self.high}")
