import os
from tempfile import NamedTemporaryFile

from .simulator import CircuitSimulator, ExecutionState
from ..backend import coreir_
from ..scope import Scope
from ..ref import DefnRef, ArrayRef, TupleRef
from ..array import ArrayType
from ..tuple import TupleType
from ..bitutils import int2seq
from ..clock import ClockType
from ..transforms import setup_clocks, flatten
from ..circuit import CircuitType
from ..uniquification import uniquification_pass, UniquificationMode

import coreir

__all__ = ['CoreIRSimulator']

def is_defn_bit(bit):
    name = bit.name
    if isinstance(name, ArrayRef):
        name = name.array.name

    return isinstance(name, DefnRef)

def convert_to_coreir_path(bit, scope):
    insts = []

    # Handle bits attached to nested definitions
    if scope.inst is not None and is_defn_bit(bit):
        defn_bit = bit
        cur_inst = scope.inst
        scope = scope.parent
        if isinstance(defn_bit.name, ArrayRef):
            bit = cur_inst.interface[defn_bit.name.array.name.name]
            bit = bit[defn_bit.name.index]
        else:
            bit = cur_inst.interface[defn_bit.name.name]

    # Build instance path to this bit
    while scope.inst is not None:
        assert(isinstance(scope.inst, CircuitType))
        inst_name = scope.inst.name
        insts.insert(0, inst_name)
        scope = scope.parent

    last_component = coreir_.magma_port_to_coreir(bit)
    last_inst, port = last_component.split('.', 1)
    insts.append(last_inst)

    # Handle renaming due to flatten types
    arrOrTuple = bit
    while isinstance(arrOrTuple.name, ArrayRef) or isinstance(arrOrTuple.name, TupleRef):
        if isinstance(arrOrTuple, ArrayType) or isinstance(arrOrTuple, TupleType):
            port, idx = port.split('.', 1)
            port += '_' + idx
        if isinstance(arrOrTuple.name, ArrayRef):
            arrOrTuple = arrOrTuple.name.array
        elif isinstance(arrOrTuple.name, TupleRef):
            arrOrTuple = arrOrTuple.name.tuple

    ports = [port]

    return insts, ports

# This exists because things like clocks and setting values doesn't have the new API
# so convert from what the new API expects to what the old API expects
def old_style_path(insts, ports):
    last_inst = insts[-1]
    return insts[:-1] + [last_inst + '.' + ports[0]]

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

class CoreIRSimulator(CircuitSimulator):
    def __get_cur_cycles(self):
        instpath, port_selects = convert_to_coreir_path(self.clock, Scope())
        steps = self.simulator_state.get_clock_cycles(old_style_path(instpath, port_selects))
        return steps

    def __get_clock_value(self):
        if self.clock is None:
            return None
        return self.get_value(self.clock, Scope())

    def __get_triggered_points(self):
        triggered = []
        for watch in self.watchpoints:
            if watch.was_triggered():
                triggered.append(watch)

        return triggered

    def __init__(self, circuit, clock, coreir_filename=None, context=None,
                 namespaces=["global"], opts={}):
        uniquification_mode_str = opts.get("uniquify", "UNIQUIFY")
        uniquification_mode = getattr(UniquificationMode,
                                      uniquification_mode_str, None)
        if uniquification_mode is None:
            raise ValueError(f"Invalid uniquification mode "
                             f"{uniquification_mode_str}")
        uniquification_pass(circuit, uniquification_mode)
        self.watchpoints = []
        self.default_scope = Scope()

        need_cleanup = False
        if not coreir_filename:
            coreir_file = NamedTemporaryFile(delete=False, suffix='.json')
            coreir_file.close()
            coreir_filename = coreir_file.name
            need_cleanup = True

        self.clock = clock
        setup_clocks(circuit)

        if context is None:
            self.ctx = coreir.Context()
        else:
            self.ctx = context
        coreir_.compile(circuit, coreir_filename, context=self.ctx)

        # Initialize interpreter, get handle back to interpreter state
        self.ctx.get_lib("commonlib")
        self.ctx.enable_symbol_table()
        coreir_circuit = self.ctx.load_from_file(coreir_filename)
        self.ctx.run_passes(["rungenerators", "wireclocks-coreir", "verifyconnectivity --noclkrst",
                             "flattentypes", "flatten", "verifyconnectivity --noclkrst", "deletedeadinstances"],
                            namespaces=namespaces)
        self.simulator_state = coreir.SimulatorState.make(coreir_circuit)

        if need_cleanup:
            os.remove(coreir_filename)

        def create_zeros_init(arrOrTuple):
            if isinstance(arrOrTuple, ArrayType):
                return [create_zeros_init(el) for el in arrOrTuple.ts]
            elif isinstance(arrOrTuple, TupleType):
                return {k: create_zeros_init(v) for k,v in zip(arrOrTuple.Ks, arrOrTuple.ts)}
            else:
                return 0

        # Need to set values for all circuit inputs or interpreter crashes
        for topin in circuit.interface.outputs():
            if not isinstance(topin, ClockType):
                arr = topin
                init = create_zeros_init(arr)

                self.set_value(topin, init, Scope())

        if clock is not None:
            insts, ports = convert_to_coreir_path(clock, Scope())
            self.simulator_state.set_main_clock(old_style_path(insts, ports))

        self.simulator_state.reset_circuit()

        for topin in circuit.interface.outputs():
            if isinstance(topin, ClockType):
                insts, ports = convert_to_coreir_path(topin, Scope())
                self.simulator_state.set_clock_value(old_style_path(insts, ports), True, False)

        self.evaluate()

    def get_capabilities(self):
        # TBD
        pass

    def get_value(self, bit, scope=None):
        if scope is None:
            scope = self.default_scope
        if bit.const():
            return True if bit == VCC else False

        # Symbol table doesn't support arrays of arrays
        if isinstance(bit, ArrayType) and (isinstance(bit[0], ArrayType) or isinstance(bit[0], TupleType)):
            r = []
            for arr in bit:
                r.append(self.get_value(arr, scope))
            return r
        elif isinstance(bit, TupleType):
            r = {}
            for k,v in zip(bit.Ks, bit.ts):
                r[k] = self.get_value(v, scope)
            return r
        else:
            insts, ports = convert_to_coreir_path(bit, scope)

            bools = self.simulator_state.get_value(insts, ports)
            if len(bools) == 1:
                return bools[0]
            return bools

    def set_value(self, bit, newval, scope=None):
        if scope is None:
            scope = self.default_scope
        if isinstance(bit, ArrayType) and len(newval) != len(bit):
                raise ValueError(f"Excepted a value of lengh {len(bit)} not"
                                 f" {len(newval)}")
        if isinstance(bit, ArrayType) and (isinstance(bit[0], ArrayType) or isinstance(bit[0], TupleType)):
            for i, arr in enumerate(bit):
                self.set_value(arr, newval[i], scope)
        elif isinstance(bit, TupleType):
            for k,v in zip(bit.Ks, bit.ts):
                self.set_value(v, newval[k], scope)
        else:
            insts, ports = convert_to_coreir_path(bit, scope)
            self.simulator_state.set_value(old_style_path(insts, ports), newval)

    def evaluate(self, no_update=False):
        clkvalue = self.__get_clock_value()
        if clkvalue is not None:
            insts, ports = convert_to_coreir_path(self.clock, Scope())
            self.simulator_state.set_clock_value(old_style_path(insts, ports), False, False)
        self.simulator_state.execute()
        if clkvalue is not None:
            self.simulator_state.set_clock_value(old_style_path(insts, ports), not clkvalue, clkvalue)

        return ExecutionState(triggered_points=self.__get_triggered_points(), clock=clkvalue, cycles=0)

    def advance(self, halfcycles=1):
        cycles = self.__get_cur_cycles()
        # TODO add a function to interpreter to avoid doing this for loop in python
        watchpoints = []
        for i in range(0, halfcycles):
            self.simulator_state.run_half_cycle()
            watchpoints = self.__get_triggered_points()
            if len(watchpoints) > 0:
                break

        post_cycles = self.__get_cur_cycles()
        return ExecutionState(triggered_points=watchpoints, clock=self.__get_clock_value(), cycles=post_cycles - cycles)

    def rewind(self, halfcycles):
        self.simulator_state.rewind(halfcycles)
        return ExecutionState(triggered_points=self.__get_triggered_points(), clock=self.__get_clock_value(), cycles=0)

    def cont(self):
        pre_cycles = self.__get_cur_cycles()
        self.simulator_state.run()
        post_cycles = self.__get_cur_cycles()
        return ExecutionState(triggered_points=self.__get_triggered_points(), clock=self.__get_clock_value(), cycles=(post_cycles - pre_cycles))

    def add_watchpoint(self, bit, scope, value=None):
        if value is None:
            raise Exception("CoreIR Simulator does not support watching for value change")

        insts, ports = convert_to_coreir_path(bit, scope)
        self.simulator_state.set_watchpoint(insts, ports, value)

        self.watchpoints.append(WatchPoint(bit, scope, self, value))

        return self.watchpoints[-1].idx

    def delete_watchpoint(self, num):
        for i, w in enumerate(self.watchpoints):
            if w.idx == num:
                insts, ports = convert_to_coreir_path(w.bit, w.scope)
                self.simulator_state.delete_watchpoint(insts, ports)
                del self.watchpoints[i]
                return True

        return False
