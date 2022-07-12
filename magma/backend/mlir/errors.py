class MlirCompilerErrorBase(RuntimeError):
    pass


class MlirCompilerInternalError(MlirCompilerErrorBase):
    pass


class MlirCompilerError(MlirCompilerErrorBase):
    pass
