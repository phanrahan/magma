from magma.backend.mlir.hw import hw
from magma.backend.mlir.mlir import push_block
from magma.backend.mlir.sv import sv


def make_mem_reg(ctx, name, N, T):
    mem_type = hw.InOutType(hw.ArrayType((N,), T))
    mem = ctx.new_value(mem_type)
    sv.RegOp(name=name, results=[mem])
    return mem


def make_mem_read(ctx, target, value, has_enable, name="read_reg"):
    if not has_enable:
        sv.ReadInOutOp(operands=[target], results=[value])
        return None, None
    reg_out = ctx.new_value(target.type.T)
    sv.ReadInOutOp(operands=[target], results=[reg_out])
    reg = ctx.new_value(target.type)
    sv.RegOp(name=name, results=[reg])
    sv.ReadInOutOp(operands=[reg], results=[value])
    return reg, reg_out


def emit_conditional_assign(target, value, en):
    with push_block(sv.IfOp(operands=[en]).then_block):
        sv.PAssignOp(operands=[target, value])


def make_index_op(ctx, value, idx):
    result = ctx.new_value(hw.InOutType(value.type.T.T))
    sv.ArrayIndexInOutOp(operands=[value, idx], results=[result])
    return result
