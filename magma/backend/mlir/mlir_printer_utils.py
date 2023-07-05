from typing import Any, Callable, List, Mapping, Union

from magma.backend.mlir.mlir import MlirAttribute, MlirValue
from magma.backend.mlir.print_opts import PrintOpts
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
        print_opts: PrintOpts,
        raw_names: bool = False,
):
    value_list = _maybe_wrap_value_or_value_list(value_or_value_list)
    get_name = get_name_fn(raw_names)

    def _make_signature(value: MlirValue) -> str:
        signature = f"{get_name(value)}: {value.type.emit()}"
        if print_opts.print_locations:
            signature += f" {value.location.emit()}"
        return signature

    printer.print(", ".join(map(_make_signature, value_list)))


def _attr_to_string(value: Any) -> str:
    if isinstance(value, MlirAttribute):
        return value.emit()
    return str(value)


def print_attr_dict(attr_dict: Mapping, printer: PrinterBase):
    attr_dict_to_string = ", ".join(
        f"{k} = {v.emit()}" for k, v in attr_dict.items()
    )
    printer.print(f"{{{attr_dict_to_string}}}")
