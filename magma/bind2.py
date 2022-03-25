from magma.circuit import DefineCircuitKind, CircuitKind
from magma.view import PortView


_BOUND_INSTANCE_INFO_KEY = "_bound_instance_info_"


def _wire_bind_arg(param, arg):
    assert param.is_input()
    if isinstance(arg, PortView):
        param @= arg
        return
    elif arg.is_output():
        param @= arg
    elif arg.is_input():
        param @= arg.value()
    elif arg.is_mixed():
        for param_i, arg_i in zip(param, arg):
            _wire_bind_arg(param_i, arg_i)
    else:
        param @= arg


def get_bound_instance_info(inst):
    return getattr(inst, _BOUND_INSTANCE_INFO_KEY, None)


def is_bound_instance(inst) -> bool:
    return get_bound_instance_info(inst) is not None


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
