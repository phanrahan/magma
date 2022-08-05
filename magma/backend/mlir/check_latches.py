from typing import Dict

from magma.t import Type
from magma.backend.mlir.sv import sv
from magma.backend.mlir.mlir import MlirValue


class LatchError(Exception):
    def __init__(self, latches, ctx):
        latches_str = ", ".join(latch.debug_name for latch in latches)
        defn_str = str(ctx.magma_defn_or_decl)
        msg = (f"Error while compiling {defn_str}, "
               f"detected potential latches: [{latches_str}]")
        super().__init__(msg)


def _get_latches_and_assigned_values(operations):
    assigned_values = set()
    latches = set()
    for op in operations:
        if isinstance(op, sv.BPAssignOp):
            assigned_values.add(op.operands[0])
        elif isinstance(op, sv.IfOp):
            then_latches, then_assigned_values = \
                _get_latches_and_assigned_values(op._then_block.operations)
            if op._else_block is not None:
                else_latches, else_assigned_values = \
                    _get_latches_and_assigned_values(op._else_block.operations)
                latches.update(then_latches.difference(assigned_values))
                latches.update(else_latches.difference(assigned_values))
                latches.update(
                    then_assigned_values.symmetric_difference(
                        else_assigned_values).difference(assigned_values))
                assigned_values.update(
                    then_assigned_values.union(else_assigned_values))
            else:
                latches.update(then_latches.difference(assigned_values))
                latches.update(
                    then_assigned_values.difference(
                        assigned_values))
    return latches, assigned_values


def check_latches(always: sv.AlwaysCombOp,
                  reg_to_val_map: Dict[MlirValue, Type],
                  ctx):
    latches, _ = _get_latches_and_assigned_values(always.body_block.operations)
    if latches:
        values = [reg_to_val_map[latch] for latch in latches]
        raise LatchError(values, ctx)
