from magma.config import config
from magma.primitives.when import WhenBuilder
from magma.passes.passes import DefinitionPass, pass_lambda


class WhenPass(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            for builder in definition._context_._builders:
                if isinstance(builder, WhenBuilder):
                    self.process_when(builder, definition)


class InferLatches(WhenPass):
    def process_when(self, builder, defn):
        builder.infer_latches()


class EmitWhenAsserts(WhenPass):
    def process_when(self, builder, defn):
        builder.emit_when_asserts()


class FinalizeWhens(WhenPass):
    def process_when(self, builder, defn):
        assert not builder._finalized
        defn._context_._placer.place(builder.finalize())


infer_latches = pass_lambda(InferLatches)
emit_when_asserts = pass_lambda(EmitWhenAsserts)
finalize_whens = pass_lambda(FinalizeWhens)


def run_when_passes(main):
    infer_latches(main)
    if config.emit_when_asserts:
        emit_when_asserts(main)
    finalize_whens(main)
