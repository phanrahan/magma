module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_div(in %a: i16, in %b: i16, out y: i16, out z: i16) {
        %0 = comb.divu %a, %b : i16
        %1 = comb.divs %a, %b : i16
        hw.output %0, %1 : i16, i16
    }
}
