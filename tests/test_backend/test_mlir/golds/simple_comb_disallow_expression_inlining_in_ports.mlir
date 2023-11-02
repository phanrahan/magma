module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_comb(in %a: i16, in %b: i16, in %c: i16, out y: i16, out z: i16) {
        %1 = hw.constant -1 : i16
        %0 = comb.xor %1, %a : i16
        %2 = comb.or %a, %0 : i16
        %3 = comb.or %2, %b : i16
        hw.output %3, %3 : i16, i16
    }
}
