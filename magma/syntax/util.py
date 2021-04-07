from typing import Optional, Mapping, Sequence, Any

from ..t import In, Out
from ..circuit import Circuit
from ..wire import wire


def build_io_args(
        annotations: Mapping[str, Any],
        output_port_names: Optional[Sequence[str]] = None,
        ) -> Mapping[str, Any]:
    io_args = {}

    for param, annotation in annotations.items():
        if param == "return":
            if isinstance(annotation, tuple):
                if output_port_names is None:
                    for i, elem in enumerate(annotation):
                        io_args[f"O{i}"] = Out(elem)
                elif len(output_port_names) == len(annotation):
                    for name, elem in zip(output_port_names, annotation):
                        if not isinstance(name, str):
                            raise TypeError(f'port names must be strings recieved {name}::{type(name)}')
                        io_args[name] = Out(elem)
                else:
                    raise ValueError(f'recieved {len(output_port_names)} names expected {len(annotation)}')
            else:
                if output_port_names is None:
                    io_args["O"] = Out(annotation)
                elif len(output_port_names) == 1:
                    io_args[output_port_names[0]] = Out(annotation)
                else:
                    raise ValueError(f'recieved {len(output_port_names)} names expected 1')

            continue
        annotation = In(annotation)
        io_args[param] = annotation
    return io_args


def build_call_args(io, annotations):
    return [getattr(io, param) for param in annotations if param != "return"]


def wire_call_result(io, call_result, annotations, output_port_names=None):
    if isinstance(call_result, Circuit):
        if not len(call_result.interface.outputs()) == 1:
            raise TypeError(
                "Expected register return instance with one output")
        call_result = call_result.interface.outputs()[0]
    if isinstance(annotations["return"], tuple):
        if output_port_names is None:
            for i in range(len(annotations["return"])):
                wire(getattr(io, f"O{i}"), call_result[i])
        else:
            for i, name in enumerate(output_port_names):
                wire(getattr(io, name), call_result[i])


    else:
        if output_port_names is None:
            wire(io.O, call_result)
        else:
            wire(getattr(io, output_port_names[0]), call_result)
