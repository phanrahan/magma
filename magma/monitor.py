from .t import In


def MonitorIO(circuit):
    IO = []
    for name, port in circuit.interface.ports.items():
        IO += [name, In(type(port))]
    return IO


def make_monitor_ports(circuit):
    return {name: In(type(port))
            for name, port in circuit.interface.ports.items()}


class MonitorGenerator:
    pass
