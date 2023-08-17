from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.when import WhenBuilder
from magma.when import _WhenBlock, _ElseWhenBlock, _OtherwiseBlock, when, elsewhen, otherwise


class WhenPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            for builder in list(definition._context_._builders):
                if isinstance(builder, WhenBuilder):
                    self.process_when_builder(builder, definition)


class InferLatches(WhenPass):
    def process_when_builder(self, builder, defn):
        builder.infer_latches()


class EmitWhenAsserts(WhenPass):
    def __init__(self, main, flatten_all_tuples):
        super().__init__(main)
        self._flatten_all_tuples = flatten_all_tuples

    def process_when_builder(self, builder, defn):
        builder.emit_when_assertions(self._flatten_all_tuples)


def _find_values_to_split(builder):
    to_split = []
    for x in builder.output_to_name.values():
        x = getattr(builder, x)
        for y in builder._input_to_name.values():
            y = getattr(builder, y)
            if y.trace() is x:
                to_split.append(x)
                break
    return to_split


def _emit_new_when_assign(value, driver_map, curr_block):
    if isinstance(curr_block, _WhenBlock):
        new_block = when(curr_block._info.condition)
    elif isinstance(curr_block, _ElseWhenBlock):
        new_block = elsewhen(curr_block._info.condition)
    elif isinstance(curr_block, _OtherwiseBlock):
        new_block = otherwise()
    with new_block:
        if curr_block in driver_map:
            value @= driver_map[curr_block]
        for child in curr_block.children():
            _emit_new_when_assign(value, driver_map, child)
    for _elsewhen in curr_block.elsewhen_blocks():
        _emit_new_when_assign(value, driver_map, _elsewhen)
    if curr_block.otherwise_block:
        _emit_new_when_assign(value, driver_map, curr_block.otherwise_block)


def _split_when_cycles(builder, defn):
    to_split = _find_values_to_split(builder)
    for value in to_split:
        driving = value.driving()
        assert len(driving) == 1
        value = driving[0]
        contexts = value._wired_when_contexts[:]
        driver_map = {}
        for ctx in contexts:
            wires = ctx.get_conditional_wires_for_drivee(value)
            assert len(wires) == 1
            driver_map[ctx] = wires[0].driver
        value.unwire()
        _emit_new_when_assign(value, driver_map, contexts[0].root)


class SplitCycles(WhenPass):
    def process_when_builder(self, builder, defn):
        _split_when_cycles(builder, defn)


class FinalizeWhens(WhenPass):
    def process_when_builder(self, builder, defn):
        assert not builder._finalized
        defn._context_._placer.place(builder.finalize())


infer_latch_pass = pass_lambda(InferLatches)
emit_when_assert_pass = pass_lambda(EmitWhenAsserts)
split_cycles_pass = pass_lambda(SplitCycles)
finalize_when_pass = pass_lambda(FinalizeWhens)


def run_when_passes(
        main,
        flatten_all_tuples: bool = False,
        emit_when_assertions: bool = False
):
    infer_latch_pass(main)
    if emit_when_assertions:
        emit_when_assert_pass(main, flatten_all_tuples)
    split_cycles_pass(main)
    finalize_when_pass(main)
