module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_custom_verilog_name_custom_name(%I: i1) -> (O: i1) {
        hw.output %I : i1
    }
}
