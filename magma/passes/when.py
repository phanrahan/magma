from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.when import WhenBuilder


class WhenPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            for builder in definition._context_._builders:
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


def _split_when_cycles(builder, defn):
    for x in builder.output_to_name.values():
        x = getattr(builder, x)
        for y in builder._input_to_name.values():
            y = getattr(builder, y)
            if y.trace() is x:
                raise Exception()


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
