module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_smart_bits(in %I: i8, out O: i8) {
        hw.output %I : i8
    }
}
