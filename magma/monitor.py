from .t import In
from .generator import Generator


def MonitorIO(circuit):
    IO = []
    for name, port in circuit.interface.ports.items():
        IO += [name, In(type(port))]
    return IO


def make_monitor_ports(circuit):
    io_dict = {}
    for name, port in circuit.interface.ports.items():
        io_dict[name] = In(type(port))
    return io_dict


class MonitorGenerator:
    pass
