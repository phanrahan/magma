import argparse
import collections
import dataclasses
import enum
import os
import re


class _Part(enum.Enum):
    MAJOR = 0
    MINOR = 1
    PATCH = 2

    @classmethod
    def choices(cls):
        return [part.name.lower() for part in cls]


@dataclasses.dataclass(frozen=True)
class _Version:
    major: int
    minor: int
    patch: int

    @staticmethod
    def parse(string: str):
        try:
            parts = string.split(".")
            parts = map(int, parts)
            return _Version(*parts)
        except:
            raise Exception(f"Could not parse '{string}' as version") from None

    def bump(self, part: _Part) -> "_Version":
        if part == _Part.MAJOR:
            return _Version(self.major + 1, 0, 0)
        if part == _Part.MINOR:
            return _Version(self.major, self.minor + 1, 0)
        if part == _Part.PATCH:
            return _Version(self.major, self.minor, self.patch + 1)

    def canonical(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __str__(self) -> str:
        return self.canonical()


class SourceBumper(collections.abc.Callable):
    def __init__(self, files):
        self._files = files
        self._modified = []

    def modified(self):
        return self._modified[:]

    @staticmethod
    def _bump_file(file_, old_version, new_version):
        try:
            with open(file_, "r") as f:
                src = f.read()
        except:
            return False
        src = src.replace(str(old_version), str(new_version))
        try:
            with open(file_, "w") as f:
                f.write(src)
        except:
            return False
        return True

    def __call__(self, old_version, new_version):
        for file_ in self._files:
            res = SourceBumper._bump_file(file_, old_version, new_version)
            if not res:
                continue
            self._modified.append(file_)


class Committer(collections.abc.Callable):
    def __init__(self, modified, msg=None):
        self._modified = modified
        self._msg = msg

    def __call__(self, old_version, new_version):
        if not self._modified:
            return
        msg = self._msg
        if msg is None:
            msg = "Relase {new_version}"
        msg = msg.format(old_version=old_version, new_version=new_version)
        os.system(f'git add {" ".join(self._modified)}')
        os.system(f'git commit -m "{msg}"')


class Tagger(collections.abc.Callable):
    def __init__(self, msg=None):
        self._msg = msg

    def __call__(self, old_version, new_version):
        msg = self._msg
        if msg is None:
            msg = "Release {new_version}"
        msg = msg.format(old_version=old_version, new_version=new_version)
        os.system(f'git tag -a v{new_version} -m "{msg}"')


def _get_version(setup_file):
    try:
        with open(setup_file) as f:
            src = f.read()
    except:
        msg = f"Could not read version from file '{setup_file}'"
        raise Exception(msg) from None
    matches = re.findall("version='[0-9].*\.[0-9].*\.[0-9].*'", src)
    if len(matches) != 1:
        msg = f"Could not read version from file '{setup_file}'"
        raise Exception(msg) from None
    version = _Version.parse(matches[0][9:-1])
    return version


def main() -> None:
    parser = argparse.ArgumentParser(description="Bump release version")
    parser.add_argument("part", type=str, choices=_Part.choices(),
                        help="version part to bump")
    parser.add_argument("--setup_file", type=str, default="setup.py",
                        help="package setup file")
    parser.add_argument("--commit", action='store_true', default=False,
                        help="perform git commit")
    parser.add_argument("--commit-msg", type=str, default="",
                        help="custom git commit message")
    parser.add_argument("--tag", action='store_true', default=False,
                        help="perform git tag")
    parser.add_argument("--tag-msg", type=str, default="",
                        help="custom git tag message")
    args = parser.parse_args()
    part = _Part[args.part.upper()]
    version = _get_version(args.setup_file)
    new_version = version.bump(part)
    # Bump source in setup.
    source_bumper = SourceBumper((args.setup_file,)) 
    source_bumper(version, new_version)
    # Commit if specified.
    if not args.commit:
        return
    commit_msg = args.commit_msg or None
    committer = Committer(source_bumper.modified(), commit_msg)
    committer(version, new_version)    
    # Commit if specified.
    if not args.tag:
        return
    tag_msg = args.tag_msg or None
    tagger = Tagger(tag_msg)
    tagger(version, new_version)    


if __name__ == "__main__":
    main()
