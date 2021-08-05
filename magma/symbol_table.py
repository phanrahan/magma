import abc
import json
from typing import Any, Iterable, Mapping, Tuple

from magma.common import make_delegator_cls


class _Sentinel:
    _instances = []

    def __init__(self, string):
        _Sentinel._instances.append(self)
        self._string = string

    @classmethod
    def match(cls, string):
        for sentinel in cls._instances:
            if sentinel.string == string:
                return sentinel
        return None

    @property
    def string(self):
        return self._string

    def __repr__(self):
        return f"_Sentinel({self._string})"

    def __str__(self):
        return self._string


SYMBOL_TABLE_INLINED_INSTANCE = _Sentinel("__SYMBOL_TABLE_INLINED_INSTANCE__")
SYMBOL_TABLE_EMPTY = _Sentinel("__SYMBOL_TABLE_EMPTY__")
InstanceNameType = Tuple[_Sentinel, str]


def _is_tuple_annotation(T):
    try:
        origin = T.__origin__
    except AttributeError:
        return False
    return origin is tuple


def _unwrap_value(value):
    if isinstance(value, tuple):
        return tuple(_unwrap_value(v) for v in value)
    if not isinstance(value, _Sentinel):
        return value
    return value.string


def _try_isinstance(value, T):
    try:
        ret = isinstance(value, T)
    except Exception:
        return None
    return ret


def _type_check_value(value, T):
    sentinel_match = _Sentinel.match(value)
    if sentinel_match is not None:
        value = sentinel_match
    if _try_isinstance(value, T) is True:
        return value
    return None


class SymbolTableInterface(abc.ABC):
    @abc.abstractmethod
    def get_module_name(self, in_module_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str) -> InstanceNameType:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_port_name(self,
                      in_module_name: str,
                      in_port_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_inlined_instance_name(self,
                                  in_module_name: str,
                                  in_parent_instance_name: str,
                                  in_child_instance_name: str) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_instance_type(self,
                          in_module_name: str,
                          in_instance_name: str) -> str:
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
                          out_instance_name: InstanceNameType) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_port_name(self,
                      in_module_name: str,
                      in_port_name: str,
                      out_port_name: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_inlined_instance_name(self,
                                  in_module_name: str,
                                  in_parent_instance_name: str,
                                  in_child_instance_name: str,
                                  out_instance_name: InstanceNameType) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_instance_type(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_type: str) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def module_names(self) -> Mapping[str, str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def instance_names(self) -> Mapping[Tuple[str, str], InstanceNameType]:
        raise NotImplementedError()

    @abc.abstractmethod
    def port_names(self) -> Mapping[Tuple[str, str], str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def inlined_instance_names(self) -> Mapping[Tuple[str, str, str],
                                                InstanceNameType]:
        raise NotImplementedError()

    @abc.abstractmethod
    def instance_types(self) -> Mapping[Tuple[str, str], str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def as_dict(self, for_json):
        raise NotImplementedError()

    @abc.abstractmethod
    def as_json(self, **kwargs):
        raise NotImplementedError()


class ImmutableSymbolTable(SymbolTableInterface):
    def set_module_name(self,
                        in_module_name: str,
                        out_module_name: str) -> None:
        raise Exception("Can not set an immutable symbol table")

    def set_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_instance_name: InstanceNameType) -> None:
        raise Exception("Can not set an immutable symbol table")

    def set_port_name(self,
                      in_module_name: str,
                      in_port_name: str,
                      out_port_name: str) -> None:
        raise Exception("Can not set an immutable symbol table")

    def set_inlined_instance_name(self,
                                  in_module_name: str,
                                  in_parent_instance_name: str,
                                  in_child_instance_name: str,
                                  out_instance_name: InstanceNameType) -> None:
        raise Exception("Can not set an immutable symbol table")

    def set_instance_type(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_type: str) -> None:
        raise Exception("Can not set an immutable symbol table")


DelegatorSymbolTable = make_delegator_cls(SymbolTableInterface)


class _FieldMeta(type):
    def __new__(metacls, name, bases, dct, info=(None, None), **kwargs):
        if "_info_" in dct:
            raise TypeError(
                "class attribute _info_ is reversed by the type machinery")
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
        assert _is_tuple_annotation(value_type)
        return len(value_type.__args__)

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
            value = _type_check_value(value, cls.value_type)
            if value is None:
                raise ValueError()
            return value
        if not isinstance(value, tuple):
            raise ValueError()
        if len(value) != cls.value_length:
            raise ValueError()
        value = tuple(_type_check_value(v, T)
                      for v, T in zip(value, cls.value_type.__args__))
        if any(v is None for v in value):
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
        return {",".join([str(ki) for ki in k]): _unwrap_value(v)
                for k, v in self._map.items()}


class SymbolTable(SymbolTableInterface):
    _fields_ = {
        "module_names": _Field[str, str],
        "instance_names": _Field[(str, str), InstanceNameType],
        "port_names": _Field[(str, str), str],
        "inlined_instance_names": _Field[(str, str, str), InstanceNameType],
        "instance_types": _Field[(str, str), str],
    }

    def __init__(self):
        self._mappings = {k: T() for k, T, in SymbolTable._fields_.items()}

    def get_module_name(self, in_module_name: str) -> str:
        return self._mappings["module_names"].get(in_module_name)

    def get_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str) -> InstanceNameType:
        key = in_module_name, in_instance_name
        return self._mappings["instance_names"].get(key)

    def get_port_name(self,
                      in_module_name: str,
                      in_port_name: str) -> str:
        key = in_module_name, in_port_name
        return self._mappings["port_names"].get(key)

    def get_inlined_instance_name(
            self,
            in_module_name: str,
            in_parent_instance_name: str,
            in_child_instance_name: str) -> InstanceNameType:
        key = in_module_name, in_parent_instance_name, in_child_instance_name
        return self._mappings["inlined_instance_names"].get(key)

    def get_instance_type(self,
                          in_module_name: str,
                          in_instance_name: str) -> str:
        key = in_module_name, in_instance_name
        return self._mappings["instance_types"].get(key)

    def set_module_name(self,
                        in_module_name: str,
                        out_module_name: str) -> None:
        self._mappings["module_names"].set(in_module_name, out_module_name)

    def set_instance_name(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_instance_name: InstanceNameType) -> None:
        key = in_module_name, in_instance_name
        self._mappings["instance_names"].set(key, out_instance_name)

    def set_port_name(self,
                      in_module_name: str,
                      in_port_name: str,
                      out_port_name: str) -> None:
        key = in_module_name, in_port_name
        self._mappings["port_names"].set(key, out_port_name)

    def set_inlined_instance_name(self,
                                  in_module_name: str,
                                  in_parent_instance_name: str,
                                  in_child_instance_name: str,
                                  out_instance_name: InstanceNameType) -> None:
        key = in_module_name, in_parent_instance_name, in_child_instance_name
        self._mappings["inlined_instance_names"].set(key, out_instance_name)

    def set_instance_type(self,
                          in_module_name: str,
                          in_instance_name: str,
                          out_type: str) -> None:
        key = in_module_name, in_instance_name
        self._mappings["instance_types"].set(key, out_type)

    def module_names(self) -> Mapping[str, str]:
        return self._mappings["module_names"].dct()

    def instance_names(self) -> Mapping[Tuple[str, str], InstanceNameType]:
        return self._mappings["instance_names"].dct()

    def port_names(self) -> Mapping[Tuple[str, str], str]:
        return self._mappings["port_names"].dct()

    def inlined_instance_names(self) -> Mapping[Tuple[str, str],
                                                InstanceNameType]:
        return self._mappings["inlined_instance_names"].dct()

    def instance_types(self) -> Mapping[Tuple[str, str], str]:
        return self._mappings["instance_types"].dct()

    def as_dict(self, for_json=False):
        return {
            name: field.dct(for_json)
            for name, field in self._mappings.items()
        }

    @staticmethod
    def from_dict(dct, from_json=False, allow_missing=True):
        table = SymbolTable()
        for name, mapping in table._mappings.items():
            T = type(mapping)
            try:
                entry = dct[name]
            except KeyError as err:
                if not allow_missing:
                    raise  # re-raise original KeyError
            else:
                table._mappings[name] = T.from_dict(entry, from_json)
        return table

    def as_json(self, **kwargs):
        return json.dumps(self.as_dict(for_json=True), **kwargs)

    @staticmethod
    def from_json(value, allow_missing=True):
        dct = json.loads(value)
        return SymbolTable.from_dict(
            dct, from_json=True, allow_missing=allow_missing)
