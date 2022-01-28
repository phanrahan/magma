from typing import Callable, List, Mapping, Union

from magma.backend.mlir.mlir import MlirValue
from magma.backend.mlir.printer_base import PrinterBase


MlirValueList = List[MlirValue]
MlirValueOrMlirValueList = Union[MlirValue, MlirValueList]


def get_name_fn(raw_names: bool) -> Callable[[MlirValue], str]:
    if raw_names:
        return lambda value: value.raw_name
    return lambda value: value.name


def _maybe_wrap_value_or_value_list(
        value_or_value_list: MlirValueOrMlirValueList) -> MlirValueList:
    if isinstance(value_or_value_list, MlirValue):
        return [value_or_value_list]
    return value_or_value_list


def print_names(
        value_or_value_list: MlirValueOrMlirValueList,
        printer: PrinterBase,
        raw_names: bool = False):
    value_list = _maybe_wrap_value_or_value_list(value_or_value_list)
    get_name = get_name_fn(raw_names)
    printer.print(", ".join(get_name(v) for v in value_list))


def print_types(
        value_or_value_list: MlirValueOrMlirValueList, printer: PrinterBase):
    value_list = _maybe_wrap_value_or_value_list(value_or_value_list)
    printer.print(", ".join(v.type.emit() for v in value_list))


def print_signature(
        value_or_value_list: MlirValueOrMlirValueList,
        printer: PrinterBase,
        raw_names: bool = False):
    value_list = _maybe_wrap_value_or_value_list(value_or_value_list)
    get_name = get_name_fn(raw_names)
    signatures = (f"{get_name(v)}: {v.type.emit()}" for v in value_list)
    printer.print(", ".join(signatures))


def print_attr_dict(attr_dict: Mapping, printer: PrinterBase):
    attr_dict_to_string = ", ".join(f"{k} = {v}" for k, v in attr_dict.items())
    printer.print(f"{{{attr_dict_to_string}}}")
