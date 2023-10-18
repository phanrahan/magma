from magma.passes.passes import DefinitionPass, pass_lambda
from magma.passes.split_when_utils import split_when_cycles
from magma.primitives.when import WhenBuilder
from magma.when import WhenBlock


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


class SplitCycles(WhenPass):
    def process_when_builder(self, builder, defn):
        split_when_cycles(builder, defn)


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
