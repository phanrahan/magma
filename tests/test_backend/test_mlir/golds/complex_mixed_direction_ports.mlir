module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @complex_mixed_direction_ports(in %a_0_x: i8, in %a_1_x: i8, in %a_2_x: i8, in %a_3_x: i8, in %a_4_x: i8, in %a_5_x: i8, in %a_6_x: i8, in %a_7_x: i8, in %b_y: i8, out a_0_y: i8, out a_1_y: i8, out a_2_y: i8, out a_3_y: i8, out a_4_y: i8, out a_5_y: i8, out a_6_y: i8, out a_7_y: i8, out b_x: i8) {
        %0 = hw.constant 0 : i8
        %1 = hw.constant 0 : i8
        %2 = hw.constant 0 : i8
        %3 = hw.constant 0 : i8
        %4 = hw.constant 0 : i8
        %5 = hw.constant 0 : i8
        %6 = hw.constant 0 : i8
        hw.output %0, %b_y, %1, %2, %3, %4, %5, %6, %a_1_x : i8, i8, i8, i8, i8, i8, i8, i8, i8
    }
}
