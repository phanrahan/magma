from magma.passes import DefinitionPass


class InsertPrefix(DefinitionPass):
    """
    Insert `prefix` before the names of all circuits
    """

    def __init__(self, main, prefix):
        super().__init__(main)
        self.prefix = prefix

    def __call__(self, definition):
        type(definition).rename(definition, self.prefix + definition.name)
