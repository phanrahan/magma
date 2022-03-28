from magma.circuit import DefineCircuitKind, CircuitKind
from magma.primitives.xmr import XMRSink, XMRSource
from magma.view import PortView


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