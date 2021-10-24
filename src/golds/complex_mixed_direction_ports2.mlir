hw.module @simple_mixed_direction_ports(%simple_mixed_direction_ports_a_x: i8) -> (%simple_mixed_direction_ports_a_y: i8) {
    hw.output %simple_mixed_direction_ports_a_x : i8
}
hw.module @complex_mixed_direction_ports2(%complex_mixed_direction_ports2_a_x: i8) -> (%complex_mixed_direction_ports2_a_y: i8) {
    %0 = hw.instance "simple_mixed_direction_ports_inst0" @simple_mixed_direction_ports(%complex_mixed_direction_ports2_a_x) : (i8) -> (i8)
    hw.output %0 : i8
}
