from .t import In
from .generator import Generator


def MonitorIO(circuit):
    IO = []
    for name, port in circuit.interface.ports.items():
        IO += [name, In(type(port))]
    return IO


class MonitorGenerator:
    pass
