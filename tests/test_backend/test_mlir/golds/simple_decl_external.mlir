module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module.extern @simple_decl(%I: i1) -> (O: i1)
    hw.module @simple_decl_external(%I: i1) -> (O: i1) {
        %0 = hw.instance "simple_decl_inst0" @simple_decl(I: %I: i1) -> (O: i1)
        hw.output %0 : i1
    }
}
