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
from magma.ref import ArrayRef, TupleRef, DerivedRef
from magma.value_utils import make_selector


class WhenCompiler:
    def __init__(self, module_visitor, module):
        self._module_visitor = module_visitor
        self._module = module
        self._operands = self._module.operands
        self._flatten_all_tuples = (
            self._module_visitor.ctx.opts.flatten_all_tuples
        )

        # Track outer_block so array_ref/constants are placed outside the always
        # comb to reduce code repetition
        self._outer_block = get_block_stack().peek()

        inst = module.module
        defn = type(inst)
        assert iswhen(defn)
        self._builder = builder = defn._builder_

        # Update index map for flattened tuples
        self._input_to_index = self._flatten_index_map(builder.input_to_index)
        self._output_to_index = self._flatten_index_map(builder.output_to_index)

        self._output_wires = self._make_output_wires()

    def _get_input_index(self, value):
        return self._input_to_index[value]

    def _get_operand(self, value):
        return self._operands[self._get_input_index(value)]

    def _flatten_index_map(self, builder_map):
        """The when builder tracks a mapping from value to their index which is
        used to find a value's position in the input port list.  This function
        flattens tuple values and updates the index map accordingly since
        flattened tuples will offset the originally indices.
        """
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
                stop_if=lambda ref: not isinstance(ref, DerivedRef)
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

        for value in sort_by_value(builder_map):
            visit_magma_value_or_value_wrapper_by_direction(
                value,
                _index_map_visit,
                _index_map_visit,
                flatten_all_tuples=self._flatten_all_tuples,
                inout_visitor=_index_map_visit
            )
        return value_to_index

    def _make_output_wires(self):
        """Create the mlir values corresponding to each output"""
        wires = [
            self._module_visitor.ctx.new_value(hw.InOutType(result.type))
            for result in self._module.results
        ]

        for result, wire in zip(self._module.results, wires):
            sv.RegOp(results=[wire])
            sv.ReadInOutOp(operands=[wire], results=[result])

        return wires

    def _flatten_value(self, value):
        fields = []
        visit_magma_value_or_value_wrapper_by_direction(
            value, fields.append, fields.append,
            flatten_all_tuples=self._flatten_all_tuples,
            inout_visitor=fields.append,
        )
        return fields

    def _get_parent(self, val, collection, to_index):
        """Search ancestor tree until we find either not an Array or we find a
        an array that is in the index map"""
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

    def _check_array_child_wire(self, val, collection, to_index):
        """If val is a child of an array in the index map, get the parent wire
        (so we add to a collection of drivers for a bulk assign)
        """
        wire, parent = self._get_parent(val, collection, to_index)
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

    def _make_operand(self, wire, index):
        """If the operand is an element of wire, emit the required array
        reference ops (extract, get, or slice) to retrieve the desired index."""
        if not index:
            return wire
        i = index[0]
        if isinstance(i, slice):
            # convert to tuple for hashing
            i = (i.start, i.stop, i.step)
        with push_block(self._outer_block):
            operand = self._module_visitor.make_array_ref(wire, i)
        return self._make_operand(operand, index[1:])

    def _build_wire_map(self, connections):
        """Collect a map of output wires to their drivers.
        If it's an array that's been elaborated, we collect the drivers in a
        dictionary using their index as a key to sort.
        """
        wire_map = {}
        for drivee, driver in connections:
            elts = zip(*map(self._flatten_value, (drivee, driver)))
            for drivee_elt, driver_elt in elts:

                operand_wire, operand_index = self._check_array_child_wire(
                    driver_elt, self._operands, self._input_to_index)
                if operand_wire:
                    operand = self._make_operand(operand_wire,
                                                 operand_index)
                else:
                    operand = self._get_operand(driver_elt)

                drivee_wire, drivee_index = self._check_array_child_wire(
                    drivee_elt, self._output_wires, self._output_to_index)
                if drivee_wire:
                    wire_map.setdefault(drivee_wire, {})
                    drivee_index = tuple(
                        i if not isinstance(i, slice) else i.start
                        for i in drivee_index
                    )
                    wire_map[drivee_wire][drivee_index] = operand
                else:
                    drivee_idx = self._output_to_index[drivee_elt]
                    drivee_wire = self._output_wires[drivee_idx]
                    wire_map[drivee_wire] = operand
        return wire_map

    def _make_arr_list(self, T):
        """Create a nested list structure matching the dimensions of T, used to
        populate the elements of an array create op"""
        if isinstance(T, builtin.IntegerType):
            return [None for _ in range(T.n)]
        assert isinstance(T, hw.ArrayType), T
        return [self._make_arr_list(T.T) for _ in range(T.dims[0])]

    def _build_array_value(self, T, value):
        """Unpack the contents of value into a nested list structure"""
        # TODO(leonardt): we could use an ndarray here, would simplify indexing
        arr = self._make_arr_list(T)
        for idx, elem in value.items():
            curr = arr
            for i in idx[:-1]:  # descend up to last index
                curr = curr[i]
            curr[idx[-1]] = elem  # use last index for setitem
        return arr

    def _combine_array_assign(self, T, value):
        """Sort drivers by index, use concat or create depending on type"""
        if isinstance(value, MlirValue):
            return value  # found whole value, no need to combine
        if all(x is None for x in value):
            return None  # found empty value, covered by previous slice
        result = self._module_visitor.ctx.new_value(T)
        if not isinstance(T, builtin.IntegerType):
            # recursive combine children
            assert len(T.dims) == 1, "Expected 1d array"
            value = [self._combine_array_assign(T.T, value[i])
                     for i in range(T.dims[0])]
        # Filter None elements (indices covered by a previous slice)
        value = [x for x in reversed(value) if x is not None]
        self._module_visitor.make_concat(value, result)
        return result

    def _make_assignments(self, connections):
        """
        * _build_wire_map: contructs mapping from output wire to driver

        * _build_array_value,
          _combine_array_assign: handle collection elaborated drivers for a bulk
                                 assign
        """
        for wire, value in self._build_wire_map(connections).items():
            if isinstance(value, dict):
                value = self._build_array_value(wire.type.T, value)
                value = self._combine_array_assign(wire.type.T, value)
            sv.BPAssignOp(operands=[wire, value])

    def _process_connections(self, block):
        connections = (
            (conditional_wire.drivee, conditional_wire.driver)
            for conditional_wire in block.conditional_wires()
        )
        self._make_assignments(connections)
        for child in block.children():
            self._process_when_block(child)

    def _process_when_block(self, block):
        """
        If no condition, we are in an otherwise case and simply emit the
        block body (which is inside a previous IfOp)

        Otherwise, we emit an IfOp with the true body corresponding to this
        block, then process the sibilings in the else block
        """
        if block.condition is None:
            return self._process_connections(block)

        cond = self._get_operand(block.condition)
        if_op = sv.IfOp(operands=[cond])

        with push_block(if_op.then_block):
            self._process_connections(block)

        curr_sibling = if_op
        with contextlib.ExitStack() as stack:
            sibling_blocks = list(block.elsewhen_blocks())
            if block.otherwise_block is not None:
                sibling_blocks.append(block.otherwise_block)
            for sibling_block in sibling_blocks:
                stack.enter_context(push_block(curr_sibling.else_block))
                curr_sibling = self._process_when_block(sibling_block)

        return if_op

    def compile(self):
        """Emit default drivers then process the when block chain"""
        with push_block(sv.AlwaysCombOp().body_block):
            self._make_assignments(self._builder.default_drivers.items())
            self._process_when_block(self._builder.block)
        return True
