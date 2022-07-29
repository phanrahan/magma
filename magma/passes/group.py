import abc
import functools
from typing import Iterable, List, Optional, Tuple

from magma.array import Array
from magma.circuit import Circuit
from magma.ref import get_ref_defn, get_ref_inst
from magma.t import Type
from magma.tuple import Tuple as m_Tuple
from magma.type_utils import isdigital, isarray, istuple


InstanceCollection = List[Circuit]
Connection = Tuple[Type, Type]


def _get_driving(value: Type) -> Iterable[Connection]:
    T = type(value)
    if isdigital(T):
        yield from ((value, drivee) for drivee in value.driving())
        return
    if not (isarray(T) or istuple(T)):
        raise TypeError(value)
    for elt in value:
        yield from _get_driving(elt)


class _GrouperBase(abc.ABC):
    def __init__(self, instances: InstanceCollection):
        self._instances = instances
        self._run = False

    @abc.abstractmethod
    def _visit_input_connection(self, driver: Type, drivee: Type):
        raise NotImplementedError()

    @abc.abstractmethod
    def _visit_output_connection(self, driver: Type, drivee: Type):
        raise NotImplementedError()

    @abc.abstractmethod
    def _visit_undriven_port(self, port: Type):
        raise NotImplementedError()

    def run(self):
        if self._run:
            raise RuntimeError("Can run grouper at most once")
        self._run_impl()
        self._run = True

    def _is_external(self, value: Type) -> Optional[bool]:
        """
        Returns whether @value is external to this group, or None if
        undecidable.
        """
        defn = get_ref_defn(value.name)
        if defn is not None:
            return True
        inst = get_ref_inst(value.name)
        if inst is not None:
            return inst not in self._instances
        assert not value.name.bound()
        return None

    def _run_on_input(self, port: Type) -> Iterable[Connection]:
        driver = port.trace()
        if driver is None:
            self._visit_undriven_port(port)
            return
        if driver.const():
            return
        is_external = self._is_external(driver)
        if is_external is not None:
            if is_external:
                yield (driver, port)
            return
        if not isinstance(port, (m_Tuple, Array)):
            raise TypeError(port)
        for elt in port:
            yield from self._run_on_input(elt)

    def _run_on_output(self, port: Type) -> Iterable[Connection]:
        for driver, drivee in _get_driving(port):
            is_external = self._is_external(drivee)
            if is_external is not None:
                if is_external:
                    yield (driver, drivee)
                continue
            raise NotImplementedError(
                f"{port}: driving annonymous value from compile guard not "
                f"supported"
            )

    def _run_on_port(self, port: Type):
        if port.is_input():
            for driver, drivee in self._run_on_input(port):
                self._visit_input_connection(driver, drivee)
        elif port.is_output():
            for driver, drivee in self._run_on_output(port):
                self._visit_output_connection(driver, drivee)
        else:  # mixed type or InOut
            if not isinstance(port, (m_Tuple, Array)):
                raise TypeError(value)

            for elt in port:
                self._run_on_port(elt)

    def _run_on_instance(self, instance: Circuit):
        for port in instance.interface.ports.values():
            self._run_on_port(port)

    def _run_impl(self):
        for instance in self._instances:
            self._run_on_instance(instance)


GrouperBase = _GrouperBase
