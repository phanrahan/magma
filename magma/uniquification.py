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
        self.mode = mode
        self.seen = {}

    def __call__(self, definition):
        name = definition.name
        if name not in self.seen:
            self.seen[name] = set()
        else:
            idx = len(self.seen[name])
            new_name = name + "_unq" + str(idx)
            type(definition).rename(definition, new_name)
        self.seen[name].add(definition)

    def _run(self, definition):
        if not isdefinition(definition):
            return

        for instance in definition.instances:
            instancedefinition = type(instance)
            if isdefinition(instancedefinition):
                self._run( instancedefinition )

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


def uniquification_pass(circuit, mode=UniquificationMode.UNIQUIFY):
    UniquificationPass(circuit, mode).run()
