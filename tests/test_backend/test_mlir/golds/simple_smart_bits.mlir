module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_smart_bits(%I: i8) -> (O: i8) {
        hw.output %I : i8
    }
}
