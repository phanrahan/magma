module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_div(%a: i16, %b: i16) -> (y: i16, z: i16) {
        %0 = comb.divu %a, %b : i16
        %1 = comb.divs %a, %b : i16
        hw.output %0, %1 : i16, i16
    }
}
