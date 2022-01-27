import sys

from mlir_to_verilog import main

if __name__ == "__main__":
    infile = None
    outfile = None
    if len(sys.argv) > 1:
        infile = sys.argv[1]
        if len(sys.argv) > 2:
            outfile = sys.argv[2]
    main(infile, outfile)
