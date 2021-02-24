import abc
import json
from typing import Any, Iterable, Tuple


class SymbolTableInterface(abc.ABC):
    @abc.abstractmethod
    def get_module_name(self, in_module_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_port_name(self,
                      in_module_name: str,
                      in_port_name: str) -> Tuple[str, str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_module_name(self,
                        in_module_name: str,
                        out_module_name: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_instance_name: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_port_name(self,
                      in_module_name: str,
                      in_port_name: str,
                      out_module_name: str,
                      out_port_name: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def as_json(self, **kwargs):
        raise NotImplementedError()


class _FieldMeta(type):
    def __new__(metacls, name, bases, dct, info=(None, None), **kwargs):
        if "_info_" in dct:
            raise TypeError("class attribute _info_ is reversed by the type machinery")
        dct['_info_'] = info
        return super().__new__(metacls, name, bases, dct, **kwargs)

    def __getitem__(cls, idx: Tuple[Any, Any]):
        metacls = type(cls)
        bases = tuple([cls])
        name = f"{cls.__name__}[{idx}]"
        t = metacls(name, bases, {}, info=(cls, idx))
        t.__module__ = cls.__module__
        return t

    @property
    def key_type(cls):
        return cls._info_[1][0]

    @property
    def key_length(cls):
        key_type = cls.key_type
        if isinstance(key_type, type):
            return 1
        assert isinstance(key_type, tuple)
        return len(key_type)

    @property
    def value_type(cls):
        return cls._info_[1][1]

    @property
    def value_length(cls):
        value_type = cls.value_type
        if isinstance(value_type, type):
            return 1
        assert isinstance(value_type, tuple)
        return len(value_type)

    def _parse_key(cls, key, from_json):
        if from_json:
            key = tuple(key.split(","))
            if len(key) == 1:
                key = key[0]
        if cls.key_length == 1:
            if not isinstance(key, cls.key_type):
                raise ValueError()
        else:
            if not isinstance(key, tuple):
                raise ValueError()
            if len(key) != cls.key_length:
                raise ValueError()
        return key

    def _parse_value(cls, value, from_json):
        if from_json:
            if isinstance(value, list):
                value = tuple(value)
        if cls.value_length == 1:
            if not isinstance(value, cls.value_type):
                raise ValueError()
        else:
            if not isinstance(value, tuple):
                raise ValueError()
            if len(value) != cls.value_length:
                raise ValueError()
        return value

    def from_dict(cls, dct, from_json=False):
        ret = cls()
        for k, v in dct.items():
            k, v = cls._parse_key(k, from_json), cls._parse_value(v, from_json)
            ret.set(k, v)
        return ret


class _Field(object, metaclass=_FieldMeta):
    def __init__(self):
        self._map = {}

    def set(self, key, value):
        try:
            self._map[key]
            raise ValueError(f"key {key} already mapped")
        except KeyError:
            pass
        self._map[key] = value

    def get(self, key):
        return self._map[key]

    def dct(self, for_json=False):
        cls = type(self)
        if not for_json or cls.key_length == 1:
            return self._map.copy()
        return {",".join([str(ki) for ki in k]): v
                for k, v in self._map.items()}


class SymbolTable(SymbolTableInterface):
    _fields_ = {
        "module_names": _Field[str, str],
        "instance_names": _Field[(str, str), str],
        "port_names": _Field[(str, str), (str, str)],
    }

    def __init__(self):
        self._mappings = {k: T() for k, T, in SymbolTable._fields_.items()}

    def get_module_name(self, in_module_name: str) -> str:
        return self._mappings["module_names"].get(in_module_name)

    def get_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str) -> str:
        key = in_module_name, in_instance_name
        return self._mappings["instance_names"].get(key)

    def get_port_name(self,
                      in_module_name: str,
                      in_port_name: str) -> Tuple[str, str]:
        key = in_module_name, in_port_name
        return self._mappings["port_names"].get(key)

    def set_module_name(self,
                        in_module_name: str,
                        out_module_name: str) -> None:
        self._mappings["module_names"].set(in_module_name, out_module_name)

    def set_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_instance_name: str) -> None:
        key = in_module_name, in_instance_name
        self._mappings["instance_names"].set(key, out_instance_name)

    def set_port_name(self,
                      in_module_name: str,
                      in_port_name: str,
                      out_module_name: str,
                      out_port_name: str) -> None:
        key = in_module_name, in_port_name
        value = out_module_name, out_port_name
        self._mappings["port_names"].set(key, value)

    def as_dict(self, for_json=False):
        return {
            name: field.dct(for_json)
            for name, field in self._mappings.items()
        }

    @staticmethod
    def from_dict(dct, from_json=False):
        table = SymbolTable()
        for name, mapping in table._mappings.items():
            T = type(mapping)
            table._mappings[name] = T.from_dict(dct[name], from_json=True)
        return table

    def as_json(self, **kwargs):
        return json.dumps(self.as_dict(for_json=True), **kwargs)

    @staticmethod
    def from_json(value):
        dct = json.loads(value)
        return SymbolTable.from_dict(dct, from_json=True)
