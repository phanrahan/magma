module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_clock_cast(in %I: i1, out O: i1) {
        hw.output %I : i1
    }
}
