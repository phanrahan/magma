module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_magma_protocol(%I: i8) -> (O: i8) {
        hw.output %I : i8
    }
    hw.module @complex_magma_protocol(%I: i8) -> (O: i8) {
        %0 = hw.instance "simple_magma_protocol_inst0" @simple_magma_protocol(I: %I: i8) -> (O: i8)
        hw.output %0 : i8
    }
}
