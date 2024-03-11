module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_aggregates_anon_product(in %a_x: i8, in %a_y: i8, out y_x: i8, out y_y: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %a_x : i8
        %2 = comb.xor %1, %a_y : i8
        hw.output %0, %2 : i8, i8
    }
}
