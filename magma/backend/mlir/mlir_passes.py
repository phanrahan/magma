import abc
from typing import Any

from magma.backend.mlir.mlir import MlirOp


class MlirOpPass(abc.ABC):
    def __init__(self, root: MlirOp):
        self._root = root
        self._callable = callable(self)

    def _run_on_op(self, op: MlirOp):
        for region in op.regions:
            for block in region.blocks:
                for op in block.operations:
                    yield from self._run_on_op(op)
                    yield self(op)

    @abc.abstractmethod
    def __call__(self, op: MlirOp) -> Any:
        raise NotImplementedError()

    def run(self):
        yield from self._run_on_op(self._root)


class CollectMlirOpsPass(MlirOpPass):
    def __call__(self, op: MlirOp):
        return op
