module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_length_one_bits(in %I: i1, out O: i1) {
        %0 = comb.concat %I : i1
        hw.output %0 : i1
    }
}
