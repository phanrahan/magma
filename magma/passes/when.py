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
    def process_when_builder(self, builder, defn):
        builder.emit_when_asserts()


class FinalizeWhens(WhenPass):
    def process_when_builder(self, builder, defn):
        assert not builder._finalized
        defn._context_._placer.place(builder.finalize())


infer_latch_pass = pass_lambda(InferLatches)
emit_when_assert_pass = pass_lambda(EmitWhenAsserts)
finalize_when_pass = pass_lambda(FinalizeWhens)


def run_when_passes(main, emit_when_asserts: bool = False):
    infer_latch_pass(main)
    if emit_when_asserts:
        emit_when_assert_pass(main)
    finalize_when_pass(main)
