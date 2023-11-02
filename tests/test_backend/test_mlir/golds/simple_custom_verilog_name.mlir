module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_custom_verilog_name_custom_name(in %I: i1, out O: i1) {
        hw.output %I : i1
    }
}
