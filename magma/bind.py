import os
from magma.array import Array
from magma.config import get_compile_dir, set_compile_dir
from magma.digital import Digital
from magma.passes.passes import CircuitPass
from magma.tuple import Tuple
from magma.verilog_utils import value_to_verilog_name


def _gen_bind_port(cls, mon_arg, bind_arg):
    if isinstance(mon_arg, Tuple) or isinstance(mon_arg, Array) and \
            not issubclass(mon_arg.T, Digital):
        result = []
        for child1, child2 in zip(mon_arg, bind_arg):
            result += _gen_bind_port(cls, child1, child2)
        return result
    port = value_to_verilog_name(mon_arg)
    arg = value_to_verilog_name(bind_arg)
    return [(f".{port}({arg})")]


def _bind(cls, monitor, compile_fn, *args):
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
        ports += _gen_bind_port(cls, mon_arg, bind_arg)
    ports_str = ",\n    ".join(ports)
    bind_str = f"bind {cls.name} {monitor.name} {monitor.name}_inst (\n    {ports_str}\n);"  # noqa
    if not os.path.isdir(".magma"):
        os.mkdir(".magma")
    curr_compile_dir = get_compile_dir()
    set_compile_dir("normal")
    # Circular dependency, need coreir backend to compile, backend imports
    # circuit (for wrap casts logic, we might be able to factor that out).
    compile_fn(f".magma/{monitor.name}", monitor, inline=True)
    set_compile_dir(curr_compile_dir)
    with open(f".magma/{monitor.name}.v", "r") as f:
        content = "\n".join((f.read(), bind_str))
    cls.bind_modules[monitor.name] = content


class BindPass(CircuitPass):
    def __init__(self, main, compile_fn):
        super().__init__(main)
        self._compile_fn = compile_fn

    def __call__(self, cls):
        if cls.bind_modules_bound:
            return
        bind_modules = cls.bind_modules.copy()
        cls.bind_modules = {}
        for monitor, args in bind_modules.items():
            _bind(cls, monitor, self._compile_fn, *args)
        cls.bind_modules_bound = True
