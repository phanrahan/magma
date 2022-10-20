module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_length_one_bits(%I: i1) -> (O: i1) {
        %0 = comb.concat %I : i1
        hw.output %0 : i1
    }
}
