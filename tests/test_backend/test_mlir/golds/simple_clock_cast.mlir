module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_clock_cast(%I: i1) -> (O: i1) {
        hw.output %I : i1
    }
}