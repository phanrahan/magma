module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_neg(in %a: i8, out y: i8) {
        %1 = hw.constant 0 : i8
        %0 = comb.sub %1, %a : i8
        hw.output %0 : i8
    }
}
