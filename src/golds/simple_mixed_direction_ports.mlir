hw.module @simple_mixed_direction_ports(%simple_mixed_direction_ports_a_0_x: i8, %simple_mixed_direction_ports_a_1_x: i8, %simple_mixed_direction_ports_a_2_x: i8, %simple_mixed_direction_ports_a_3_x: i8, %simple_mixed_direction_ports_a_4_x: i8, %simple_mixed_direction_ports_a_5_x: i8, %simple_mixed_direction_ports_a_6_x: i8, %simple_mixed_direction_ports_a_7_x: i8, %simple_mixed_direction_ports_b_y: i8) -> (%simple_mixed_direction_ports_a_0_y: i8, %simple_mixed_direction_ports_a_1_y: i8, %simple_mixed_direction_ports_a_2_y: i8, %simple_mixed_direction_ports_a_3_y: i8, %simple_mixed_direction_ports_a_4_y: i8, %simple_mixed_direction_ports_a_5_y: i8, %simple_mixed_direction_ports_a_6_y: i8, %simple_mixed_direction_ports_a_7_y: i8, %simple_mixed_direction_ports_b_x: i8) {
    %0 = hw.constant 0 : i8
    %1 = hw.constant 0 : i8
    %2 = hw.constant 0 : i8
    %3 = hw.constant 0 : i8
    %4 = hw.constant 0 : i8
    %5 = hw.constant 0 : i8
    %6 = hw.constant 0 : i8
    hw.output %0, %simple_mixed_direction_ports_b_y, %1, %2, %3, %4, %5, %6, %simple_mixed_direction_ports_a_1_x : i8, i8, i8, i8, i8, i8, i8, i8, i8
}
