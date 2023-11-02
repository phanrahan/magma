module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_magma_protocol(in %I: i8, out O: i8) {
        hw.output %I : i8
    }
}
