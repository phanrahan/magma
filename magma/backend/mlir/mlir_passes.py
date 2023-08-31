import abc

from magma.backend.mlir.mlir import MlirOp


class MlirOpPass:
    def __init__(self, root: MlirOp):
        self._root = root
        self._callable = callable(self)

    def _run_on_op(self, op: MlirOp):
        for region in op.regions:
            for block in region.blocks:
                for op in block.operations:
                    yield from self._run_on_op(op)
                    if self._callable:
                        yield self(op)

    def run(self):
        yield from self._run_on_op(self._root)


class CollectMlirOpsPass(MlirOpPass):
    def __call__(self, op: MlirOp):
        return op
