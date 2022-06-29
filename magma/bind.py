import os
from magma.bit import Bit
from magma.bits import Bits
from magma.array import Array
from magma.config import get_compile_dir, set_compile_dir
from magma.digital import Digital
from magma.passes.passes import CircuitPass
from magma.primitives.wire import Wire
from magma.tuple import Tuple
from magma.verilog_utils import value_to_verilog_name, is_nd_array
from magma.ref import TempNamedRef, AnonRef
from magma.t import Direction
from magma.conversions import from_bits, as_bits
from magma.view import PortView, InstView
from magma.wire import wire
from magma.inline_verilog import _get_view_inst_parent


def _should_disable_ndarray(mon_arg, bind_arg):
    if isinstance(bind_arg, PortView):
        bind_arg = bind_arg.port

    if (isinstance(mon_arg, Array) and
            isinstance(bind_arg.name.root(), (TempNamedRef, AnonRef))):

        # Disable NDArray logic for temporary since CoreIR Wire primitive (used
        # for temporaries) does not support ndarrays yet (root() is not None
        # for Named temporary values)
        return True
    return False


def _gen_bind_port(cls, mon_arg, bind_arg):
    if (isinstance(mon_arg, Tuple) or isinstance(mon_arg, Array) and not
            is_nd_array(type(mon_arg))):
        result = []
        for child1, child2 in zip(mon_arg, bind_arg):
            result += _gen_bind_port(cls, child1, child2)
        return result
    port = value_to_verilog_name(mon_arg, False)
    arg = value_to_verilog_name(
        bind_arg, _should_disable_ndarray(mon_arg, bind_arg))
    return [(f".{port}({arg})")]


def _wire_temp(bind_arg, temp):
    if bind_arg.is_mixed():
        for x, y in zip(bind_arg, temp):
            _wire_temp(x, y)
        return
    if bind_arg.is_input():
        bind_arg = bind_arg.value()
        if bind_arg is None:
            raise ValueError("Cannot bind undriven input")
    wire(bind_arg, temp)


def _bind(cls, monitor, compile_fn, user_namespace, verilog_prefix,
          compile_guard, *args):
    bind_str = monitor.verilogFile
    ports = []
    for mon_arg, cls_arg in zip(monitor.interface.ports.values(),
                                cls.interface.ports.values()):
        if str(mon_arg.name) != str(cls_arg.name):
            error_str = f"""
Bind monitor interface does not match circuit interface
    Monitor Ports: {list(monitor.interface.ports)}
    Circuit Ports: {list(cls.interface.ports)}
"""
            raise TypeError(error_str)
        ports += _gen_bind_port(cls, mon_arg, cls_arg)
    extra_mon_args = list(
        monitor.interface.ports.values()
    )[len(cls.interface):]
    for mon_arg, bind_arg in zip(extra_mon_args, args):
        if isinstance(bind_arg, PortView):
            T = type(bind_arg.port)
            parent = _get_view_inst_parent(bind_arg).parent
            if isinstance(parent, InstView):
                defn = parent.circuit
            else:
                assert isinstance(parent, Circuit)
                defn = type(parent)
            driver = bind_arg.port
        else:
            T = type(bind_arg)
            defn = cls
            driver = bind_arg
        with defn.open():
            if not hasattr(defn, "num_bind_wires"):
                defn.num_bind_wires = 0
            name = f"_magma_bind_wire_{defn.num_bind_wires}"
            defn.num_bind_wires += 1
            temp = T.qualify(Direction.Undirected)(name=name)
            _wire_temp(driver, temp)
            temp.unused()
        if isinstance(bind_arg, PortView):
            temp = PortView[type(temp)](temp, bind_arg.parent.parent)
        bind_arg = temp
        ports += _gen_bind_port(cls, mon_arg, bind_arg)
    ports_str = ",\n    ".join(ports)
    cls_name = cls.name
    monitor_name = monitor.name
    if user_namespace is not None:
        cls_name = user_namespace + "_" + cls_name
        monitor_name = user_namespace + "_" + monitor_name
    if verilog_prefix is not None:
        cls_name = verilog_prefix + cls_name
        monitor_name = verilog_prefix + monitor_name
    bind_str = f"bind {cls_name} {monitor_name} {monitor_name}_inst (\n    {ports_str}\n);"  # noqa
    if compile_guard is not None:
        bind_str = f"""
`ifdef {compile_guard}
{bind_str}
`endif
"""
    if not os.path.isdir(".magma"):
        os.mkdir(".magma")
    curr_compile_dir = get_compile_dir()
    set_compile_dir("normal")
    # Circular dependency, need coreir backend to compile, backend imports
    # circuit (for wrap casts logic, we might be able to factor that out).
    compile_fn(f".magma/{monitor.name}", monitor, inline=True,
               user_namespace=user_namespace, verilog_prefix=verilog_prefix)
    set_compile_dir(curr_compile_dir)
    with open(f".magma/{monitor.name}.v", "r") as f:
        content = "\n".join((f.read(), bind_str))
    cls.compiled_bind_modules[monitor.name] = content


class BindPass(CircuitPass):
    def __init__(self, main, compile_fn, user_namespace, verilog_prefix):
        super().__init__(main)
        self._compile_fn = compile_fn
        self.user_namespace = user_namespace
        self.verilog_prefix = verilog_prefix

    def __call__(self, cls):
        for monitor, (args, compile_guard) in cls.bind_modules.items():
            _bind(cls, monitor, self._compile_fn, self.user_namespace,
                  self.verilog_prefix, compile_guard, *args)
