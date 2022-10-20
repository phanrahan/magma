module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @simple_verilog_defn(%I: i1) -> (O: i1)
    hw.module @simple_verilog_defn_wrapper(%I: i1) -> (O: i1) {
        %0 = hw.instance "simple_verilog_defn_inst0" @simple_verilog_defn(I: %I: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
