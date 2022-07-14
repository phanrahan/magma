import contextlib
import dataclasses
import io
import pathlib


_TMP_ROOT_DIR = ".magma"


def _make_tmp_root_dir() -> pathlib.Path:
    path = pathlib.Path(_TMP_ROOT_DIR)
    path.mkdir(exist_ok=True)
    return path


@dataclasses.dataclass(frozen=True)
class _TemporaryDirectory:
    path: pathlib.Path

    @property
    def name(self) -> str:
        return str(self.path)


@contextlib.contextmanager
def TemporaryDirectory():
    try:
        path = _make_tmp_root_dir()
        yield _TemporaryDirectory(path)
    finally:
        pass


def NamedTemporaryFile(name: str, *args, **kwargs):
    path = _make_tmp_root_dir() / pathlib.Path(name)
    return path.open(*args, **kwargs)
