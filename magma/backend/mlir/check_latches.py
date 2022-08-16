from typing import Dict, List

from magma.t import Type
from magma.backend.mlir.sv import sv
from magma.backend.mlir.mlir import MlirValue, MlirOp


class LatchError(Exception):
    def __init__(self, latches, ctx):
        latches_str = ", ".join(latch.debug_name for latch in latches)
        defn_str = str(ctx.magma_defn_or_decl)
        msg = (f"Error while compiling {defn_str}, "
               f"detected potential latches: [{latches_str}]")
        super().__init__(msg)


def _get_latches_and_assigned_values(operations: List[MlirOp], reg_to_val_map,
                                     cond_to_when_map):
    """
    latches: A list of values that are potential latches (not assigned in all
             branches).
    assigned_values: A list of values that are assigned inside `operations`.

    Note: this is a conservative check that requires values are assigned in
    every case.  For example, there may be an unreachable case where a value is
    not assigned, but that requires symbolic evaluation to discover.  In
    general, symbolic evaluation is difficult, but may be viable in the
    hardware domain where we may have less issues with path explosion,
    aliasing, arrays, etc...
    """
    latches = set()
    assigned_values = set()

    for op in operations:
        if isinstance(op, sv.BPAssignOp):
            assigned_values.add(op.operands[0])  # update assigned values
        elif isinstance(op, sv.IfOp):
            # Recursively check if then block
            then_latches, then_assigned_values = \
                _get_latches_and_assigned_values(op._then_block.operations, reg_to_val_map, cond_to_when_map)
            # Different logic depending on whether there's an else.
            if op._else_block is not None:
                else_latches, else_assigned_values = \
                    _get_latches_and_assigned_values(op._else_block.operations, reg_to_val_map, cond_to_when_map)
                # Latches are propagated upwards if they aren't assigned inside
                # this block (i.e. have a default value).
                latches.update(then_latches.difference(assigned_values))
                latches.update(else_latches.difference(assigned_values))
                # Add latches for values assigned in one branch buat not the
                # other.
                latches.update(
                    then_assigned_values.symmetric_difference(
                        else_assigned_values).difference(assigned_values))
                # Update assigned values with those assigned in both branches
                assigned_values.update(
                    then_assigned_values.union(else_assigned_values))
            else:
                # If no else, we simply add latches for any latches inside
                # then_latches without a default value
                latches.update(then_latches.difference(assigned_values))
                # Also add latches for anything assigned in then that do not
                # have a default value
                latches.update(
                    then_assigned_values.difference(
                        assigned_values))
            when = cond_to_when_map[op.operands[0]]

            def f(latch):
                val = reg_to_val_map[latch]
                if val._enclosing_when_cond_stack and (val._enclosing_when_cond_stack[-1] == when):
                    return False
                return True
            latches = set(filter(f, latches))
    return latches, assigned_values


def check_latches(always: sv.AlwaysCombOp,
                  reg_to_val_map: Dict[MlirValue, Type],
                  cond_to_when_map,
                  ctx):
    latches, _ = _get_latches_and_assigned_values(always.body_block.operations,
                                                  reg_to_val_map,
                                                  cond_to_when_map)
    if latches:
        values = [reg_to_val_map[latch] for latch in latches]
        raise LatchError(values, ctx)
