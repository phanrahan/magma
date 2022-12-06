module attributes {circt.loweringOptions = "locationInfoStyle=plain"} {
    hw.module @simple_comb(%a: i16, %b: i16, %c: i16) -> (y: i16, z: i16) {
        %1 = hw.constant -1 : i16
        loc(unknown)
        %0 = comb.xor %1, %a : i16
        loc(unknown)
        %2 = comb.or %a, %0 : i16
        loc(unknown)
        %3 = comb.or %2, %b : i16
        loc(unknown)
        hw.output %3, %3 : i16, i16
        loc(unknown)
    }
    loc(unknown)
}
loc(unknown)
