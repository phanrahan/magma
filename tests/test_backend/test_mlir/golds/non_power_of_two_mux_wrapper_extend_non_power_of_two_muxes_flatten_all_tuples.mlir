module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @non_power_of_two_mux_wrapper(%a_x: i8, %a_y: i1, %s: i4) -> (y_x: i8, y_y: i1) {
        %1 = hw.constant -1 : i8
        %0 = comb.xor %1, %a_x : i8
        %3 = hw.constant -1 : i1
        %2 = comb.xor %3, %a_y : i1
        %6 = hw.array_create %0, %0, %0, %0, %0, %0, %0, %0, %0, %0, %0, %0, %0, %0, %0, %a_x : i8
        %4 = hw.array_get %6[%s] : !hw.array<16xi8>, i4
        %7 = hw.array_create %2, %2, %2, %2, %2, %2, %2, %2, %2, %2, %2, %2, %2, %2, %2, %a_y : i1
        %5 = hw.array_get %7[%s] : !hw.array<16xi1>, i4
        hw.output %4, %5 : i8, i1
    }
}
