import argparse
import dataclasses
import logging
import os
import sys
from typing import Dict

from magma.backend.mlir.mlir_to_verilog import mlir_to_verilog, MlirToVerilogOpts
from magma.common import slice_opts


logging.basicConfig(level=os.environ.get("LOGLEVEL", "WARNING").upper())


def _field_to_argument_params(field: dataclasses.Field) -> Dict:
    if field.default_factory is not dataclasses.MISSING:
        raise TypeError(field)
    params = {
        "required": field.default is dataclasses.MISSING,
    }
    if field.type is bool and not params["required"] and not field.default:
        params.update({"action": "store_true"})
        return params
    if not params["required"]:
        params.update({"default": field.default})
    params.update({
        "action": "store",
        "type": field.type,
    })
    return params


def _add_dataclass_arguments(parser: argparse.ArgumentParser, cls: type):
    assert dataclasses.is_dataclass(cls)
    for field in dataclasses.fields(cls):
        params = _field_to_argument_params(field)
        parser.add_argument(f"--{field.name}", **params)


def main(prog_args = None) -> int:
    parser = argparse.ArgumentParser(
        "Compile a (MLIR) .mlir file to verilog (.v/.sv)"
    )

    parser.add_argument(
        "infile",
        metavar="<input filename>",
        action="store",
        type=str,
        help="Input MLIR file",
    )
    parser.add_argument(
        "--outfile",
        metavar="<output filename>",
        action="store",
        type=argparse.FileType("w"),
        required=False,
        default=sys.stdout,
    )
    _add_dataclass_arguments(parser, MlirToVerilogOpts)

    args = parser.parse_args(prog_args)
    opts = slice_opts(vars(args), MlirToVerilogOpts)
    
    logging.debug(f"Running with opts: {opts}")
    if opts.split_verilog and args.outfile is not sys.stdout:
        logging.warning(
            f"outfile ({args.outfile.name}) likely ignored with split_verilog "
            f"enabled"
        )

    with open(args.infile, "r") as f_in:
        mlir_to_verilog(f_in, args.outfile, opts)


if __name__ == "__main__":
    exit(main())
    
