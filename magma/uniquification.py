from enum import Enum, auto
from .is_definition import isdefinition
from .logging import warning, error
from .passes import DefinitionPass


class MultipleDefinitionException(Exception):
    pass


class UniquificationMode(Enum):
    WARN = auto()
    ERROR = auto()
    UNIQUIFY = auto()


class UniquificationPass(DefinitionPass):
    def __init__(self, main, mode):
        super(UniquificationPass, self).__init__(main)
        self.definitions = {}
        self.mode = mode
        self.seen = {}
        self.original_names = {}

    def __call__(self, definition):
        name = definition.name
        key = hash(repr(definition))

        if name not in self.seen:
            self.seen[name] = {}
        if key not in self.seen[name]:
            if self.mode is UniquificationMode.UNIQUIFY and len(self.seen[name]) > 0:
                new_name = name + "_unq" + str(len(self.seen[name]))
                type(definition).rename(definition, new_name)
            self.seen[name][key] = [definition]
        else:
            if self.mode is not UniquificationMode.UNIQUIFY:
                assert self.seen[name][key][0].name == definition.name
            else:
                type(definition).rename(definition, self.seen[name][key][0].name)
            self.seen[name][key].append(definition)

    def _run(self, definition):
        if not isdefinition(definition):
            return

        for instance in definition.instances:
            instancedefinition = type(instance)
            if isdefinition(instancedefinition):
                self._run( instancedefinition )

        id_ = id(definition)
        if id_ in self.definitions:
            return
        self.definitions[id_] = definition
        self(definition)

    def run(self):
        super(UniquificationPass, self).run()
        duplicated = []
        for name, definitions in self.seen.items():
            if len(definitions) > 1:
                duplicated.append((name, definitions))
        UniquificationPass.handle(duplicated, self.mode)

    @staticmethod
    def handle(duplicated, mode):
        if len(duplicated):
            msg = f"Multiple definitions: {[name for name, _ in duplicated]}"
            if mode is UniquificationMode.ERROR:
                error(msg)
                raise MultipleDefinitionException([name for name, _ in duplicated])
            elif mode is UniquificationMode.WARN:
                warning(msg)


# This pass runs uniquification according to @mode and returns a dictionary
# mapping any renamed circuits to their original names. If @mode is ERROR or
# WARN the returned dictionary should be empty.
def uniquification_pass(circuit, mode):
    pass_ = UniquificationPass(circuit, mode)
    pass_.run()
    return pass_.original_names
