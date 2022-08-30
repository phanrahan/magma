from magma.passes.passes import DefinitionPass, pass_lambda
from magma.primitives.when import WhenBuilder


class FinalizeWhensPass(DefinitionPass):
    """
    Should be called as the last pass in the compiler since other passes could
    introduce conditional assignments
    """

    def __call__(self, definition):
        if isinstance(definition, WhenBuilder):
            pass


finalize_whens = pass_lambda(FinalizeWhensPass)
