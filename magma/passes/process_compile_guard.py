from collections import defaultdict
from magma.interface import IO
from magma.circuit import Circuit
from magma.clock import Clock, AbstractReset
from magma.passes.passes import DefinitionPass
from magma.wire import wire


class ProcessCompileGuardPass(DefinitionPass):
    def _process_compile_guard(self, circuit, compile_guard, instances):
        # Collect drivers produced inside the compile guard
        internal_drivers = set()
        for instance in instances:
            for port in instance.interface.outputs():
                internal_drivers.add(port)
        # Collect drivers produced outside the compile guard
        external_drivers = set()
        # Also collect undriven ports with defaults (e.g. clock)
        default_drivers = {}
        for instance in instances:
            for port in instance.interface.inputs(True):
                # TODO: what about non whole intermediates that might be driven
                # from a combination of external and internal?
                driver = port.trace()
                if driver is None:
                    # TODO Need to support array/tuple of clocks
                    # Assert here and expect a previous pass has detect
                    # undriven ports
                    assert isinstance(port, (Clock, AbstractReset))
                    default_drivers[type(port)] = str(port.name)
                    continue

                if driver not in internal_drivers and not driver.const():
                    external_drivers.add(driver)

        class _CompileGuardWrapper(Circuit):
            ports = {}
            for driver in external_drivers:
                ports[driver.name.qualifiedname("_")] = type(driver).flip()
            for T, _name in default_drivers.items():
                ports[_name] = T

            io = IO(**dict(sorted(ports.items())))
            new_internal_driver_map = {}
            new_instances = []
            for old_inst in instances:
                new_inst = type(old_inst)(name=old_inst.name)
                new_instances.append(new_inst)
                for _name, port in old_inst.interface.ports.items():
                    if not port.isoutput():
                        continue
                    new_internal_driver_map[port] = getattr(new_inst, _name)

            for new_inst, old_inst in zip(new_instances, instances):
                for _name, port in old_inst.interface.ports.items():
                    if not port.isinput():
                        continue
                    driver = port.trace()
                    if driver is None:
                        # Unwired, e.g. clock
                        continue
                    if driver in external_drivers:
                        new_driver = getattr(io, driver.name.qualifiedname("_"))
                    elif driver.const():
                        new_driver = driver
                    else:
                        new_driver = new_internal_driver_map[driver]
                    wire(new_driver, getattr(new_inst, _name))
        with circuit.open():
            inst = _CompileGuardWrapper()
            for driver in external_drivers:
                wire(driver, getattr(inst, driver.name.qualifiedname("_")))
            inst.coreir_metadata = {"compile_guard": compile_guard.guard_str}

    def __call__(self, circuit):
        compile_guard_instances = defaultdict(list)
        new_instances = []
        for inst in circuit.instances:
            if inst.compile_guard is not None:
                # TODO: We should verify that no guarded instances are used to
                # drive something outside of the compile guard
                compile_guard_instances[inst.compile_guard].append(inst)
            else:
                new_instances.append(inst)
        # TODO: Ideally we have an API to remove instances
        circuit._context_.placer._instances = new_instances
        for compile_guard, instances in compile_guard_instances.items():
            self._process_compile_guard(circuit, compile_guard, instances)
