from abc import ABC, abstractmethod
import ast
from collections import Counter
import inspect
import textwrap
from .config import get_debug_mode
from .view import InstView


class PlacerBase(ABC):
    @abstractmethod
    def place(self, inst):
        raise NotImplementedError()

    @abstractmethod
    def instances(self):
        raise NotImplementedError()

    def finalize(self):
        return


class Placer:
    def __init__(self, defn):
        self._defn = defn
        self._instances = []
        self._instance_counter = Counter()
        self._name_counter = Counter()
        self._name_to_instance = {}

    def _inspect_name(self, inst):
        # Try to fetch instance name.
        with open(inst.debug_info.filename, "r") as f:
            line = f.read().splitlines()[inst.debug_info.lineno - 1]
            tree = ast.parse(textwrap.dedent(line)).body[0]
            # Simple case when <Name> = <Instance>().
            if isinstance(tree, ast.Assign) and len(tree.targets) == 1 \
                    and isinstance(tree.targets[0], ast.Name):
                name = tree.targets[0].id
                # Handle case when we've seen a name multiple times (e.g. reused
                # inside a loop).
                if self._name_counter[name] == 0:
                    inst.name = name
                    self._name_counter[name] += 1
                else:
                    if self._name_counter[name] == 1:
                        # Append `_0` to the first instance with this name.
                        orig = self._name_to_instance[name]
                        orig.name += "_0"
                        del self._name_to_instance[name]
                        self._name_to_instance[orig.name] = orig
                    inst.name = f"{name}_{self._name_counter[name]}"
                    self._name_counter[name] += 1

    def instances(self):
        return self._instances

    def place(self, inst):
        """Place a circuit instance in this definition"""
        if not inst.name:
            if get_debug_mode():
                self._inspect_name(inst)
            if not inst.name:
                # Default name if we could not find one or debug mode is off.
                inst_count = self._instance_counter[type(inst).name]
                inst.name = f"{type(inst).name}_inst{str(inst_count)}"
                self._instance_counter[type(inst).name] += 1
                self._name_counter[inst.name] += 1
        else:
            self._name_counter[inst.name] += 1
        for sub_inst in getattr(type(inst), "instances", []):
            setattr(inst, sub_inst.name, InstView(sub_inst, inst))
        self._name_to_instance[inst.name] = inst
        inst.defn = self._defn
        if get_debug_mode():
            inst.stack = inspect.stack()
        self._instances.append(inst)
