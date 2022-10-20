module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_neg(%a: i8) -> (y: i8) {
        %1 = hw.constant 0 : i8
        %0 = comb.sub %1, %a : i8
        hw.output %0 : i8
    }
}
