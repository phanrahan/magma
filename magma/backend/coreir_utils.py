from collections import OrderedDict
import json
from hwtypes import BitVector
from ..array import ArrayMeta, Array
from ..bit import VCC, GND, BitIn, DigitalMeta
from ..clock import (wiredefaultclock, wireclock, Clock, AsyncReset,
                     AsyncResetN, Reset)
from ..ref import ArrayRef, DefnRef, TupleRef, InstRef
from ..tuple import Tuple, TupleMeta
from .util import make_relative


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
        return f"{array_name}.{name.index}"
    if isinstance(name, TupleRef):
        tuple_name = magma_name_to_coreir_select(name.tuple.name)
        key_name = _tuple_key_to_string(name.index)
        return f"{tuple_name}.{key_name}"
    raise NotImplementedError(name)


def magma_port_to_coreir_port(port):
    return magma_name_to_coreir_select(port.name)


def check_magma_type(port, error_msg=""):
    if isinstance(port, ArrayMeta):
        msg = error_msg.format("Array({}, {})").format(str(port.N), "{}")
        check_magma_type(port.T, msg)
        return
    if isinstance(port, TupleMeta):
        for (k, t) in zip(port.keys(), port.types()):
            msg = error_msg.format("Tuple({}:{})".format(k, "{}"))
            check_magma_type(t, msg)
        return
    if isinstance(port, DigitalMeta):
        return
    raise CoreIRBackendError(error_msg.format(str(port)))


def check_magma_interface(interface):
    # For now only allow Bit, Array, or Tuple.
    for name, port in interface.ports.items():
        check_magma_type(type(port), "Type {} not supported by CoreIR backend")


def magma_type_to_coreir_type(context, type_):
    if issubclass(type_, Array):
        return context.Array(type_.N,
                             magma_type_to_coreir_type(context, type_.T))
    if issubclass(type_, Tuple):
        zipped = zip(type_.keys(), type_.types())
        return context.Record({
            _tuple_key_to_string(k): magma_type_to_coreir_type(context, t)
            for (k, t) in zipped
        })
    if type_.isinput():
        if issubclass(type_, Clock):
            return context.named_types[("coreir", "clk")]
        if issubclass(type_, (AsyncReset, AsyncResetN)):
            return context.named_types[("coreir", "arst")]
        return context.Bit()
    if type_.isoutput():
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


def add_non_input_ports(non_input_ports, port):
    if not port.isinput():
        non_input_ports[port] = magma_port_to_coreir_port(port)
    if isinstance(port, (Tuple, Array)):
        for element in port:
            add_non_input_ports(non_input_ports, element)


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


def is_clock_or_nested_clock(p):
    if isinstance(p, Clock) or isinstance(p, type) and issubclass(p, Clock):
        return True
    if isinstance(p, (Array, ArrayMeta)):
        return is_clock_or_nested_clock(p.T)
    if isinstance(p, (Tuple, TupleMeta)):
        for item in p.Ts:
            if is_clock_or_nested_clock(item):
                return True
    return False


def attach_debug_info(coreir_obj, debug_info, a=None, b=None):
    def fn(k, v):
        if a and b:
            return coreir_obj.add_metadata(a, b, k, v)
        return coreir_obj.add_metadata(k, v)

    fn("filename", json.dumps(make_relative(debug_info.filename)))
    fn("lineno", json.dumps(str(debug_info.lineno)))


def map_genarg(context, value):
    if isinstance(value, type) and issubclass(value, Clock):
        if value.isinput():
            return context.named_types[("coreir", "clkIn")]
        return context.named_types[("coreir", "clk")]
    if isinstance(value, type) and issubclass(value, (AsyncReset, AsyncResetN)):
        if value.isinput():
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


def is_const(array):
    return all(x in {VCC, GND} for x in array)


def constant_to_value(constant):
    if constant is GND:
        return 0
    if constant is VCC:
        return 1
    if isinstance(constant, Array):
        values = [constant_to_value(c) for c in constant]
        return BitVector[len(constant)](values)
    raise NotImplementedError(constant)
