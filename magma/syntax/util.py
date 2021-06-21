from typing import Optional, Mapping, Sequence, Any

from ..t import In, Out
from ..circuit import Circuit
from ..wire import wire


def build_output_port_names(
        annotations: Mapping[str, Any],
        output_port_names: Optional[Sequence[str]] = None,
    ) -> Sequence[str]:

    try:
        r_type = annotations['return']
    except KeyError:
        raise ValueError('No return annotation') from None

    if output_port_names is None:
        output_port_names = []
        if isinstance(r_type, tuple):
            for i, _ in enumerate(r_type):
                output_port_names.append(f'O{i}')
        else:
            output_port_names.append('O')
    elif isinstance(r_type, tuple):
        if len(r_type) != len(output_port_names):
            raise ValueError(f'recieved {len(output_port_names)} names expected {len(annotation)}')
    elif len(output_port_names) != 1:
        raise ValueError(f'recieved {len(output_port_names)} names expected 1')

    return output_port_names


def build_io_args(
        annotations: Mapping[str, Any],
        output_port_names: Optional[Sequence[str]] = None,
        ) -> Mapping[str, Any]:
    io_args = {}

    output_port_names = build_output_port_names(annotations, output_port_names)

    for param, annotation in annotations.items():
        if param == "return":
            if isinstance(annotation, tuple):
                for name, elem in zip(output_port_names, annotation):
                    if not isinstance(name, str):
                        raise TypeError(f'port names must be strings recieved {name}::{type(name)}')
                    io_args[name] = Out(elem)
            else:
                io_args[output_port_names[0]] = Out(annotation)

            continue
        annotation = In(annotation)
        io_args[param] = annotation
    return io_args


def build_call_args(io, annotations):
    return [getattr(io, param) for param in annotations if param != "return"]


def wire_call_result(io, call_result, annotations, output_port_names=None):
    output_port_names = build_output_port_names(annotations, output_port_names)

    if isinstance(call_result, Circuit):
        if not len(call_result.interface.outputs()) == 1:
            raise TypeError(
                "Expected register return instance with one output")
        call_result = call_result.interface.outputs()[0]

    if isinstance(annotations["return"], tuple):
        for i, name in enumerate(output_port_names):
            wire(getattr(io, name), call_result[i])
    else:
        wire(getattr(io, output_port_names[0]), call_result)
