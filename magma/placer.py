from abc import ABC, abstractmethod
import ast
from collections import Counter
import inspect
import textwrap
from .config import get_debug_mode
from .ref import LazyCircuit
from .view import InstView


def _parse_name(inst):
    """
    Returns 'name' if the source where @inst is instanced looks like:

      <name> = <type>(...)

    otherwise, returns None.
    """
    try:
        # File may not exist (e.g. in sequential we exec a string)
        with open(inst.debug_info.filename, "r") as f:
            line = f.read().splitlines()[inst.debug_info.lineno - 1]
            tree = ast.parse(textwrap.dedent(line)).body[0]
    except Exception:
        # Sometimes we cannot parse the line, e.g.
        # x = [Circuit()
        #      for _ in range(8)]
        # Will give use the second line for the list comprehension, which
        # cannot be parsed.  It's probably generally difficult to catch all
        # these cases
        # For now, we just silently ignore exceptions and just assume we can't
        # find a good debug name
        return None
    # Simple case when <Name> = <Instance>().
    if isinstance(tree, ast.Assign) and len(tree.targets) == 1 \
       and isinstance(tree.targets[0], ast.Name):
        return tree.targets[0].id
    return None


class PlacerBase(ABC):
    @abstractmethod
    def place(self, inst):
        raise NotImplementedError()

    @abstractmethod
    def instances(self):
        raise NotImplementedError()

    @abstractmethod
    def is_staged(self) -> bool:
        raise NotImplementedError()


def _setup_view(inst):
    inst_view = InstView(inst)
    # Setup view now because inline strings might use it during defn
    for sub_inst in getattr(type(inst), "instances", []):
        setattr(inst, sub_inst.name, InstView(sub_inst, inst_view))


class Placer:
    def __init__(self, defn):
        self._defn = defn
        self._name_counter = Counter()
        self._instance_counter = Counter()
        self._instance_name_map = {}
        self._instances = []
        self._finalized = False

    @property
    def name(self):
        return self._defn.name

    def instances(self):
        return self._instances

    def _user_name(self, inst) -> bool:
        """
        Returns True if @inst already has a name, False otherwise. Does not
        modify @inst in either case.
        """
        if not inst.name:
            return False
        self._name_counter[inst.name] += 1
        return True

    def _debug_name(self, inst) -> bool:
        """
        Tries to retrieve a debug name from the source of the instance; sets the
        name of @inst and returns True if available. Otherwise (or if debug mode
        is disabled), returns False.
        """
        if not get_debug_mode():
            return False
        basename = _parse_name(inst)
        if not basename:
            return False
        count = self._name_counter[basename]
        inst.name = basename if count == 0 else f"{basename}_{count}"
        # If this is the first duplicate of basename we've seen (e.g. in a
        # second-iteration of a loop), then we need to rename the first instance
        # with a appended '_0'.
        if count == 1:
            first = self._instance_name_map[basename]
            first.name += "_0"
            del self._instance_name_map[basename]
            self._instance_name_map[first.name] = first
        self._name_counter[basename] += 1
        return True

    def _definition_name(self, inst) -> bool:
        """
        Sets name of @inst based on the type of @inst, of the form
        {type.name}_inst{count}. Always returns True.
        """
        type_name = type(inst).name
        count = self._instance_counter[type_name]
        inst.name = f"{type_name}_inst{count}"
        self._name_counter[inst.name] += 1
        self._instance_counter[type_name] += 1
        return True

    def _name(self, inst):
        # Sets the name of @inst by delegating to methods _user_name,
        # _debug_name, _definition_name. Note that because the 'or' is
        # short-circuited, we call as many of these as needed until one returns
        # True. We expect exactly one to return True, and assert that.
        assert (self._user_name(inst)
                or self._debug_name(inst)
                or self._definition_name(inst))
        self._instance_name_map[inst.name] = inst

    def place(self, inst):
        self._name(inst)
        self._instances.append(inst)
        inst.defn = self._defn
        if get_debug_mode():
            inst.stack = inspect.stack()
        _setup_view(inst)

    def is_staged(self) -> bool:
        return False

    def finalize(self, defn):
        if self._finalized:
            raise Exception("Can only call finalize on a placer once")
        self._finalized = True
        return self


class StagedPlacer(ABC):
    def __init__(self, name):
        self._name = name
        self._instances = []
        self._finalized = False

    @property
    def instances(self):
        return self._instances.copy()

    @property
    def name(self):
        return self._name

    def place(self, inst):
        self._instances.append(inst)
        inst.defn = LazyCircuit
        _setup_view(inst)

    def is_staged(self) -> bool:
        return True

    def finalize(self, defn):
        if self._finalized:
            raise Exception("Can only call finalize on a staged placer once")
        placer = Placer(defn)
        for inst in self._instances:
            placer.place(inst)
        self._finalized = True
        return placer
