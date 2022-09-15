from magma.primitives.when import WhenBuilder
from magma.passes.passes import DefinitionPass, pass_lambda


class FinalizeWhens(DefinitionPass):
    def __call__(self, definition):
        with definition.open():
            for builder in definition._context_._builders:
                if isinstance(builder, WhenBuilder) and not builder._finalized:
                    definition._context_._placer.place(builder.finalize())


finalize_whens = pass_lambda(FinalizeWhens)
