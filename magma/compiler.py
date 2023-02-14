from abc import abstractmethod


__all__ = ["Compiler", "make_compiler"]


class Compiler:
    def __init__(self, main, basename, opts={}):
        self.main = main
        self.basename = basename
        self.opts = opts

    def run_pre_uniquification_passes(self):
        pass

    def compile(self):
        suffix = self.suffix()
        code = self.generate_code()
        with open(f"{self.basename}.{suffix}", "w") as f:
            f.write(code)

    @abstractmethod
    def suffix(self):
        raise NotImplementedError()

    @abstractmethod
    def generate_code(self):
        raise NotImplementedError()


def make_compiler(suffix, code_generator):
    class _NewCompiler(Compiler):
        def suffix(self):
            return suffix

        def generate_code(self):
            return code_generator(self.main)

    return _NewCompiler
