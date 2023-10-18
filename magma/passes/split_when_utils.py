from magma.when import (
    when,
    elsewhen,
    otherwise,
    WhenBlock,
    ElseWhenBlock,
    OtherwiseBlock
)


def _check_to_split(value, outputs, to_split):
    source = value.trace()
    for elem in source.root_iter():
        if any(elem is output for output in outputs):
            to_split.append(source)
            return
    if value.has_children() and value.has_elaborated_children():
        for _, child in value.enumerate_children():
            _check_to_split(child, outputs, to_split)


def _get_builder_ports(builder, names):
    """Filter out removed ports."""
    return [getattr(builder, name) for name in names if hasattr(builder, name)]


def _find_values_to_split(builder):
    """Detect output values that feed into inputs."""
    to_split = []
    outputs = _get_builder_ports(builder, builder.output_to_name.values())
    inputs = _get_builder_ports(builder, builder.input_to_name.values())
    for value in inputs:
        _check_to_split(value, outputs, to_split)
    return to_split


def _emit_new_when_assign(value, driver_map, curr_block):
    """Reconstruct when logic in new set of blocks."""
    if isinstance(curr_block, WhenBlock):
        new_block = when(curr_block._info.condition)
    elif isinstance(curr_block, ElseWhenBlock):
        new_block = elsewhen(curr_block._info.condition)
    elif isinstance(curr_block, OtherwiseBlock):
        new_block = otherwise()
    with new_block:
        if curr_block in driver_map:
            for driver in driver_map[curr_block]:
                value @= driver
        for child in curr_block.children():
            _emit_new_when_assign(value, driver_map, child)
    for _elsewhen in curr_block.elsewhen_blocks():
        _emit_new_when_assign(value, driver_map, _elsewhen)
    if curr_block.otherwise_block:
        _emit_new_when_assign(value, driver_map, curr_block.otherwise_block)


def _build_driver_map(drivee):
    # driver_map stores the driver for each context that drivee is driven.
    driver_map = {}
    for ctx in drivee._wired_when_contexts:
        wires = ctx.get_conditional_wires_for_drivee(drivee)
        driver_map[ctx] = (wire.driver for wire in wires)
    return driver_map


def split_when_cycles(builder, defn):
    to_split = _find_values_to_split(builder)
    for value in to_split:
        driving = value.driving()
        driver_map = _build_driver_map(driving[0])
        for drivee in driving:
            drivee.unwire()
            root = next(iter(driver_map.keys())).root
            _emit_new_when_assign(drivee, driver_map, root)
