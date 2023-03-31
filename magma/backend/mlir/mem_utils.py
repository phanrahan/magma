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


def collect_multiport_memory_operands(
    operands, start_idx, num_ports, num_operands_per_port
):
    """Collect flat list of operands for read or write ports.
    start_idx: offset in `operands` list to start from
    num_ports: number of ports to collect
    num_operands_per_port: number of operands per port
                           (e.g. 3 for waddr, wdata, wen)
    """
    port_operands = []
    curr_idx = start_idx
    for i in range(num_ports):
        port_operands.append(
            operands[curr_idx:curr_idx + num_operands_per_port]
        )
        curr_idx += num_operands_per_port
    return port_operands


def make_multiport_memory_index_ops(ctx, ports, mem):
    """For each port, emit an array index op and return a list of results."""
    return [make_index_op(ctx, mem, port[0]) for port in ports]


def make_multiport_memory_read_ops(
        ctx, read_results, read_ports, read_ports_out
):
    """If ren, emit an intermediate register to hold read value."""
    read_targets = []
    for i, (target, port) in enumerate(zip(read_results, read_ports)):
        has_en = len(port) == 2
        read_reg, read_temp = make_mem_read(
            ctx, target, read_ports_out[i], has_en, f"read_reg_{i}"
        )
        if has_en:
            read_targets.append((read_reg, read_temp, port[1]))
    return read_targets


def emit_conditional_assigns(targets):
    for target, data, en in targets:
        emit_conditional_assign(target, data, en)
