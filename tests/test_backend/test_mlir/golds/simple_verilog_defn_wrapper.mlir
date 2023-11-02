module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module.extern @simple_verilog_defn(in %I: i1, out O: i1)
    hw.module @simple_verilog_defn_wrapper(in %I: i1, out O: i1) {
        %0 = hw.instance "simple_verilog_defn_inst0" @simple_verilog_defn(I: %I: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
