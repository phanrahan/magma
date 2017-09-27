import sys
from abc import abstractmethod
if sys.version_info < (3, 4):
    import abc
    ABC = abc.ABCMeta('ABC', (object,), {})
else:
    from abc import ABC
from collections import namedtuple
from itertools import product
from .simulator import CircuitSimulator, ExecutionState
from ..transforms import flatten, setup_clocks
from ..circuit import *
from ..scope import *
from ..bit import VCC, GND, BitType, _BitType
from ..array import ArrayType
from ..bits import SIntType, BitsType
from ..bit_vector import BitVector
from ..bitutils import seq2int
from ..clock import ClockType

__all__ = ['PythonSimulator', 'testvectors']

ExecutionOrder = namedtuple('ExecutionOrder', ['stateful', 'combinational'])


class PythonSimulatorException(Exception):
    pass


class SimPrimitive:
    def __init__(self, primitive, value_store):
        if primitive.simulate is None:
            raise ValueError("Cannot simulate {} of type {} because it does not have a Python simulate method".format(primitive, type(primitive)))
        self.primitive = primitive
        self.inputs = []
        self.outputs = []
        self.value_store = value_store
        self.state_store = {}

        for bit in self.primitive.interface.ports.values():
            if not isinstance(bit, ArrayType):
                bit = [bit]
            for b in bit:
                if b.isinput():
                    self.inputs.append(b)
                else:
                    self.outputs.append(b)

    def stateful(self):
        return self.primitive.stateful

    def inputs_satisfied(self):
        for i in self.inputs:
            if not self.value_store.value_initialized(i):
                return False

        return True

    def initialize_outputs(self):
        # Initializes all outputs to False, should perhaps
        # initialize based on starting inputs?
        for o in self.outputs:
            self.value_store.set_value(o, False)

    def simulate(self):
        self.primitive.simulate(self.value_store, self.state_store)

class WatchPoint:
    idx = 0
    def __init__(self, bit, scope, simulator, value):
        self.bit = bit
        self.scope = scope
        self.simulator = simulator
        self.value = value
        self.old_val = self.simulator.get_value(self.bit, self.scope)

        WatchPoint.idx += 1
        self.idx = WatchPoint.idx

    def was_triggered(self):
        new_val = self.simulator.get_value(self.bit, self.scope)
        triggered = new_val != self.old_val 
        if self.value:
            if self.value != new_val:
                triggered = False
        self.old_val = new_val

        return triggered

class ValueStore:
    def __init__(self):
        self.value_map = {}

    def value_initialized(self, bit):
        if isinstance(bit, ArrayType):
            for b in bit:
                if not self.value_initialized(b):
                    return False

            return True

        if bit.isinput():
            bit = bit.value()

        if bit.const():
            return True

        return bit in self.value_map

    def get_value(self, bit):
        if isinstance(bit, ArrayType):
            return [self.get_value(b) for b in bit]

        if bit.isinput():
            bit = bit.value()

        if bit.const():
            return True if bit == VCC else False

        return self.value_map[bit]

    def set_value(self, bit, newval):
        if isinstance(bit, ArrayType):
            if isinstance(newval, BitVector):
                newval = newval.as_bool_list()
            elif isinstance(newval, BitsType):
                if not newval.const():
                    raise ValueError("Calling set_value with a BitsType only works with a constant")
                newval = newval.bits()
            for b,v in zip(bit, newval):
                self.set_value(b, v)
            return

        if isinstance(newval, BitVector):
            assert len(newval) == 1
            newval = newval.as_bool_list()[0]
        assert isinstance(newval, bool), "Can only set boolean values"
        assert bit.isoutput()

        self.value_map[bit] = newval

class PythonSimulator(CircuitSimulator):
    def __setup_primitives(self):
        wrapped = []
        for primitive in self.circuit.instances:
            wrapped.append(SimPrimitive(primitive, self.value_store))

        return wrapped

    def __setup_circuit(self, clock):
        if clock is not None:
            clock = self.txfm.get_new_bit(clock, self.default_scope)
        self.clock = clock

        self.circuit_inputs = []
        self.circuit_outputs = []
        for name, bit in self.circuit.interface.ports.items():
            if not isinstance(bit, ArrayType):
                bit = [bit]
            for b in bit:
                if b.isoutput():
                    self.circuit_inputs.append(b)
                    self.value_store.set_value(b, False)
                else:
                    self.circuit_outputs.append(b)

    def __outputs_initialized(self):
        for bit in self.circuit_outputs:
            assert bit.isinput()
            if not self.value_store.value_initialized(bit):
                return False

        return True

    def __sort_state_primitives(self, state_primitives):
        """
        State primitives should be sorted in reversed topological order.
        This ensures that the simulation order of the stateful elements
        is correct.
        Intuition:
            If the output value of a state element `x` feeds into the input of
            another state element `y`,
            `y` should perform it's simulation before `x` because it will use
            the value of the signal on the previous clock cycle.
        """
        sorted_state_primitives = []
        for primitive_1 in state_primitives:
            inserted = False
            for index, primitive_2 in enumerate(sorted_state_primitives):
                for output in primitive_1.inputs:
                    if output.value() in primitive_2.inputs:
                        sorted_state_primitives.insert(index, primitive_1)
                        inserted = True
                        break
                if inserted:
                    break
            if not inserted:
                sorted_state_primitives.append(primitive_1)
        sorted_state_primitives.reverse()
        return sorted_state_primitives

    def __get_ordered_primitives(self, unordered_primitives):
        state_primitives = []
        after_state = []

        state_primitives = []
        for primitive in unordered_primitives:
            if primitive.stateful():
                primitive.initialize_outputs()
                state_primitives.append(primitive)

        sorted_state_primitives = self.__sort_state_primitives(state_primitives)

        unordered_primitives[:] = [u for u in unordered_primitives if not u.stateful()]

        combinational = []
        while len(unordered_primitives) > 0:
            found = False
            for primitive in unordered_primitives:
                if primitive.inputs_satisfied():
                    primitive.initialize_outputs()
                    combinational.append(primitive)
                    unordered_primitives.remove(primitive)
                    found = True
                    break
            assert found, "Some circuits have unsatisfied inputs"
        
        return ExecutionOrder(stateful=sorted_state_primitives, combinational=combinational)

    def __init__(self, main_circuit, clock=None):
        if isinstance(main_circuit, CircuitType):
            raise ValueError("PythonSimulator must be called with a Circuit definition, not an instance")
        if clock is not None and not isinstance(clock, ClockType):
            raise ValueError("clock must be a ClockType or None")
        setup_clocks(main_circuit)
        self.main_circuit = main_circuit
        self.txfm = flatten(main_circuit)
        self.circuit = self.txfm.circuit
        self.value_store = ValueStore()
        self.default_scope = Scope()
        self.__setup_circuit(clock)
        self.watchpoints = []

        primitives = self.__setup_primitives()

        self.execution_order = self.__get_ordered_primitives(primitives)

        assert self.__outputs_initialized(), "All circuit outputs not initialized."

    def get_capabilities(self):
        return []

    def get_value(self, bit, scope=None):
        if scope is None:
            scope = self.default_scope
        newbit = self.txfm.get_new_bit(bit, scope)
        if newbit is None:
            return None

        try:
            return self.value_store.get_value(newbit)
        except KeyError:
            return None

    def set_value(self, bit, newval, scope=None):
        if scope is None:
            scope = self.default_scope
        newbit = self.txfm.get_new_bit(bit, scope)
        if not self.is_circuit_input(newbit):
            message = "Only setting main's inputs is supported (Trying to set: {})".format(bit)
            raise PythonSimulatorException(message)
        else:
            self.value_store.set_value(newbit, newval)

    def is_circuit_input(self, value):
        """
        Checks if `value` is in `self.circuit_inputs`.
        If `value` is an `ArrayType`, it recursively checks the elements
        """
        if isinstance(value, _BitType):
            return value in self.circuit_inputs
        elif isinstance(value, ArrayType):
            return all(self.is_circuit_input(elem) for elem in value)
        else:
            raise NotImplementedError(type(value))

    def evaluate(self):
        for primitive in self.execution_order.stateful:
            primitive.simulate()
        for primitive in self.execution_order.combinational:
            primitive.simulate()

        triggered = []
        for watch in self.watchpoints:
            if watch.was_triggered():
                triggered.append(watch)

        return ExecutionState(triggered_points=triggered, clock=self.get_clock_value(), cycles=0)

    def get_clock_value(self):
        """
        Looks up the value of `self.clock` in `self.value_store`
        Returns None if self.clock is None (circuit doesn't have a clock)
        """
        if self.clock is not None:
            return self.value_store.get_value(self.clock)
        return None

    def step(self):
        if self.clock is None:
            raise PythonSimulatorException("Cannot step a simulated circuit "
                    "without a clock, did you pass a clock during "
                    "initialization?")
        cur_clock_val = self.value_store.get_value(self.clock)
        self.value_store.set_value(self.clock, not cur_clock_val)

    def cont(self):
        cycles = 0
        while True:
            self.step()
            state = self.evaluate()
            if not state.clock:
                cycles += 1

            if state.triggered_points:
                return ExecutionState(triggered_points=state.triggered_points, clock=state.clock, cycles=cycles)

    def add_watchpoint(self, bit, scope, value=None):
        self.watchpoints.append(WatchPoint(bit, scope, self, value))
        return self.watchpoints[-1].idx

    def delete_watchpoint(self, num):
        for w in self.watchpoints:
            if w.idx == num:
                del w
                return True

        return False

    def __call__(self, *largs):
        circuit = self.main_circuit

        j = 0
        for name, port in circuit.interface.ports.items():
            if port.isoutput():
                n = 1
                if isinstance(port, ArrayType):
                    n = type(port).N
                val = BitVector(largs[j], num_bits=n)
                self.set_value(getattr(circuit, name), val)
                j += 1

        self.evaluate()

        outs = []
        for name, port in circuit.interface.ports.items():
            if port.isinput():
                val = self.get_value(getattr(circuit, name))
                val = int(val) if isinstance(val, bool) else seq2int(val)
                outs.append(val)

        if len(outs) == 1:
            return outs[0]
        return tuple(outs)


def testvectors(circuit, input_ranges=None, mode='complete'):
    ntest = len(circuit.interface.ports.items())

    simulator = PythonSimulator(circuit)

    args = []
    for i, (name, port) in enumerate(circuit.interface.ports.items()):
        if port.isoutput():
            if isinstance(port, BitType):
                args.append([BitVector(0),BitVector(1)])
            elif isinstance(port, ArrayType):
                num_bits = type(port).N
                if isinstance(port, SIntType):
                    if input_ranges is None:
                        start = -2**(num_bits - 1)
                        end = 2**(num_bits - 1)  # We don't subtract one because range end is exclusive
                        input_range = range(start, end)
                    else:
                        input_range = input_ranges[i]
                    args.append([BitVector(x, num_bits=num_bits) for x in input_range])
                else:
                    if input_ranges is None:
                        input_range = range(1<<num_bits)
                    else:
                        input_range = input_ranges[i]
                    args.append([BitVector(x, num_bits=num_bits) for x in input_range])
            else:
                assert True, "can't test Tuples"

    tests = []
    for test in product(*args):
        test = list(test)
        testv = ntest*[0]
        j = 0
        for i, (name, port) in enumerate(circuit.interface.ports.items()):
            # circuit defn output is an input to the idefinition
            if port.isoutput(): 
                testv[i] = test[j].as_int()
                val = test[j].as_bool_list()
                if len(val) == 1: val = val[0]
                simulator.set_value(getattr(circuit, name), val)
                j += 1

        simulator.evaluate()

        for i, (name, port) in enumerate(circuit.interface.ports.items()):
            # circuit defn input is an input of the definition
            if port.isinput():
                val = simulator.get_value(getattr(circuit, name))
                val = int(val) if isinstance(val, bool) else seq2int(val)
                testv[i] = val


        tests.append(testv)

    return tests

