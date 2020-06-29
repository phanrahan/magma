from ..t import In, Out
from ..circuit import Circuit
from ..wire import wire


def build_io_args(annotations):
    io_args = {}

    for param, annotation in annotations.items():
        if param == "return":
            if isinstance(annotation, tuple):
                for i, elem in enumerate(annotation):
                    io_args[f"O{i}"] = Out(elem)
            else:
                io_args["O"] = Out(annotation)
            continue
        annotation = In(annotation)
        io_args[param] = annotation
    return io_args


def build_call_args(io, annotations):
    return [getattr(io, param) for param in annotations if param != "return"]


def wire_call_result(io, call_result, annotations):
    if isinstance(call_result, Circuit):
        if not len(call_result.interface.outputs()) == 1:
            raise TypeError(
                "Expected register return instance with one output")
        call_result = call_result.interface.outputs()[0]
    if isinstance(annotations["return"], tuple):
        for i in range(len(annotations["return"])):
            wire(getattr(io, f"O{i}"), call_result[i])
    else:
        wire(io.O, call_result)
