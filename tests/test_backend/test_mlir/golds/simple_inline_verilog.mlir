module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_inline_verilog(in %I: i1, out O: i1) {
        %0 = hw.constant 0 : i1
        sv.verbatim "\n\t// This is 'a' \"comment\".\n" (%0) : i1
        hw.output %I : i1
    }
}
