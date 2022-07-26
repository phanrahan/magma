from magma.is_definition import isdefinition
from magma.passes.passes import EditDefinitionPass, pass_lambda


def _terminate_if_unwired_output(port):
    if port.is_mixed():
        # list comp so it doesn't short circuit
        terminated = [_terminate_if_unwired_output(p) for p in port]
        return any(terminated)
    if port.is_output() and not port.wired():
        port.unused()
        return True
    return False


def _terminate_unused(interface):
    terminated = False
    for port in interface.ports.values():
        terminated |= _terminate_if_unwired_output(port)
    return terminated


class TerminateUnusedPass(EditDefinitionPass):
    def edit(self, circuit):
        if _terminate_unused(circuit.interface):
            circuit._is_definition = True
        if not isdefinition(circuit):
            return
        for inst in circuit.instances:
            _terminate_unused(inst.interface)


terminate_unused = pass_lambda(TerminateUnusedPass)
