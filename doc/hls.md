# High-level synthesis with RHEA-HLS

RHEA-HLS is the high-level synthesis backend of RHEA, 
a system for analyzing programs as state machines.

RHEA-HLS takes a Scheme-like functional program as input,
and then generates a CPUGEN program (RTL).

## Usage

Set the environment variable `MAGMA_BIN` to the `bin` subdirectory of this repo,
and then add `MAGMA_BIN` to your `PATH`:

    export PATH=$MAGMA_BIN:$PATH

The RHEA-relevant binaries/scripts `rhea-hls[.exe], makehls`, and `hls.py` will become available.

Suppose the filename of the program to synthesize is `basename.ss`.

### Footer file

The resulting CPUGEN file will be called `basename_hls.ss`.
As CPUGEN operates on `*.ss` files, turning them into Magma files (`.py`),
in order to interface with the rest of Magma, the file `basename_hls_footer.py`
must be available in the same directory as the `basename_hls.ss` file.

See `test6/cpugen/hls/simple_loop_hls_footer.py` for an example.

### Compiling to Magma

After the footer is created, we can now use RHEA-HLS to perform high-level synthesis.
To do this, issue

    makehls name/of/prog/basename

Indeed, the argument to makecpu can contain directories,
but it must end with `<name-of-program>.ss`.

