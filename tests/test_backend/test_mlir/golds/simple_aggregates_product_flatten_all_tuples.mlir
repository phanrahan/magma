module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_aggregates_product(%a_x: i8, %a_y: i8) -> (y_x: i8, y_y: i8) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %a_x : i8
        %2 = comb.xor %1, %a_y : i8
        hw.output %0, %2 : i8, i8
    }
}
