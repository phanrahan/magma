import contextlib
import itertools

from magma.backend.mlir.builtin import builtin
from magma.backend.mlir.hw import hw
from magma.backend.mlir.magma_common import (
    visit_value_or_value_wrapper_by_direction as
    visit_magma_value_or_value_wrapper_by_direction,
)
from magma.backend.mlir.mlir import get_block_stack, MlirValue, push_block
from magma.backend.mlir.sv import sv
from magma.common import sort_by_value
from magma.primitives.when import iswhen
from magma.ref import ArrayRef, TupleRef
from magma.value_utils import make_selector


class WhenCompiler:

    def _flatten_index_map(self, builder_map):
        value_to_index = {}
        counter = itertools.count()

        def _index_map_visit(value):
            nonlocal counter, value_to_index
            if isinstance(value.name, TupleRef) and value in value_to_index:
                # tuples are flattened by the
                # `visit_magma_value_or_value_wrapper_by_direction`, so we avoid
                # adding them twice which invalidates the count logic
                return
            for ref in value.name.root_iter(
                stop_if=lambda ref: not isinstance(ref, (ArrayRef, TupleRef))
            ):
                if ref.parent_value in value_to_index:
                    # Don't add, only need its parent
                    return

            # NOTE(leonardt): value may already be in value_to_index, in which
            # case we update it to a new index.  This is okay and it just means
            # that `value` occurs as more than one input (for example, it could
            # be used as a conditional driver for multiple values).  We could
            # optimize the logic to always share the same argument, but for now
            # we just use the "last" index.
            value_to_index[value] = next(counter)

        flatten_all_tuples = self._module_visitor._ctx.opts.flatten_all_tuples
        for value in sort_by_value(builder_map):
            visit_magma_value_or_value_wrapper_by_direction(
                value,
                _index_map_visit,
                _index_map_visit,
                flatten_all_tuples=flatten_all_tuples,
                inout_visitor=_index_map_visit
            )
        return value_to_index

    def __init__(self, module_visitor, module):
        self._module_visitor = module_visitor

        inst = module.module
        defn = type(inst)
        assert iswhen(defn)
        self.builder = builder = defn._builder_
        input_to_index = self._flatten_index_map(self.builder.input_to_index)
        output_to_index = self._flatten_index_map(self.builder.output_to_index)

        wires = [
            self._module_visitor._ctx.new_value(hw.InOutType(result.type))
            for result in module.results
        ]
        for result, wire in zip(module.results, wires):
            sv.RegOp(results=[wire])
            sv.ReadInOutOp(operands=[wire], results=[result])

        # Track outer_block so array_ref/constants are placed outside the always
        # comb to reduce code repetition
        outer_block = get_block_stack().peek()

        flatten_all_tuples = self._module_visitor._ctx.opts.flatten_all_tuples

        def _collect_visited(value):
            fields = []
            visit_magma_value_or_value_wrapper_by_direction(
                value, fields.append, fields.append,
                flatten_all_tuples=flatten_all_tuples,
                inout_visitor=fields.append,
            )
            return fields

        def _get_parent(val, collection, to_index):
            for ref in val.name.root_iter(
                stop_if=lambda ref: not isinstance(ref, ArrayRef)
            ):
                try:
                    idx = to_index[ref.array]
                except KeyError:
                    pass  # try next parent
                else:
                    return collection[idx], ref.array
            return None, None  # didn't find parent

        def _check_array_child_wire(val, collection, to_index):
            """If val is a child of an array, get the root wire
            (so we add to a collection of drivers for a bulk assign)
            """
            wire, parent = _get_parent(val, collection, to_index)
            if wire is None:
                return None, None

            class _IndexBuilder:
                def __init__(self):
                    self.index = tuple()

                def __getitem__(self, idx):
                    self.index += (idx, )
                    return self

            builder = _IndexBuilder()
            make_selector(val, stop_at=parent).select(builder)
            return wire, builder.index

        def _make_operand(wire, index):
            if not index:
                return wire
            i = index[0]
            if isinstance(i, slice):
                # convert to tuple for hashing
                i = (i.start, i.stop, i.step)
            with push_block(outer_block):
                operand = self._module_visitor.make_array_ref(wire, i)
            return _make_operand(operand, index[1:])

        def _build_wire_map(connections):
            """Collect a map of output wires to their drivers.
            If it's an array that's been elaborated, we collect the drives in a
            dictionary using their index as a key to sort.
            """
            wire_map = {}
            for drivee, driver in connections:
                elts = zip(*map(_collect_visited, (drivee, driver)))
                for drivee_elt, driver_elt in elts:

                    operand_wire, operand_index = _check_array_child_wire(
                        driver_elt, module.operands, input_to_index)
                    if operand_wire:
                        operand = _make_operand(operand_wire, operand_index)
                    else:
                        operand = module.operands[input_to_index[driver_elt]]

                    drivee_wire, drivee_index = _check_array_child_wire(
                        drivee_elt, wires, output_to_index)
                    if drivee_wire:
                        wire_map.setdefault(drivee_wire, {})
                        drivee_index = tuple(
                            i if not isinstance(i, slice) else i.start
                            for i in drivee_index
                        )
                        wire_map[drivee_wire][drivee_index] = operand
                    else:
                        drivee_wire = wires[output_to_index[drivee_elt]]
                        wire_map[drivee_wire] = operand
            return wire_map

        def _make_arr(T):
            if isinstance(T, builtin.IntegerType):
                return [None for _ in range(T.n)]
            assert isinstance(T, hw.ArrayType), T
            return [_make_arr(T.T) for _ in range(T.dims[0])]

        def _build_array_value(T, value):
            arr = _make_arr(T)
            for idx, elem in value.items():
                curr = arr
                for i in idx[:-1]:
                    curr = curr[i]
                curr[idx[-1]] = elem
            return arr

        def _combine_array_assign(T, value):
            """Sort drivers by index, use concat or create depending on type"""
            if isinstance(value, MlirValue):
                return value
            if all(x is None for x in value):
                return None
            result = self._module_visitor._ctx.new_value(T)
            operands = value
            if not isinstance(T, builtin.IntegerType):
                # recursive combine children
                assert len(T.dims) == 1, "Expected 1d array"
                operands = [_combine_array_assign(T.T, value[i])
                            for i in range(T.dims[0])]
            # Filter None elements (indices covered by a previous slice)
            operands = [x for x in reversed(operands) if x is not None]
            self._module_visitor._make_concat(operands, result)
            return result

        def _make_assignments(connections):
            for wire, value in _build_wire_map(connections).items():
                if isinstance(value, dict):
                    value = _build_array_value(wire.type.T, value)
                    value = _combine_array_assign(wire.type.T, value)
                sv.BPAssignOp(operands=[wire, value])

        def _process_when_block(block):
            connections = (
                (conditional_wire.drivee, conditional_wire.driver)
                for conditional_wire in block.conditional_wires()
            )
            if block.condition is None:
                _make_assignments(connections)
                for child in block.children():
                    _process_when_block(child)
                return
            cond = module.operands[input_to_index[block.condition]]
            if_op = sv.IfOp(operands=[cond])
            with push_block(if_op.then_block):
                _make_assignments(connections)
                for child in block.children():
                    _process_when_block(child)
            curr_sibling = if_op
            with contextlib.ExitStack() as stack:
                sibling_blocks = list(block.elsewhen_blocks())
                if block.otherwise_block is not None:
                    sibling_blocks.append(block.otherwise_block)
                for sibling_block in sibling_blocks:
                    stack.enter_context(push_block(curr_sibling.else_block))
                    curr_sibling = _process_when_block(sibling_block)
            return if_op

        with push_block(sv.AlwaysCombOp().body_block):
            _make_assignments(builder.default_drivers.items())
            _process_when_block(builder.block)

    def compile(self):
        return True
