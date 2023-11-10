module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_mixed_direction_ports(in %a_x: i8, out a_y: i8) {
        hw.output %a_x : i8
    }
    hw.module @complex_mixed_direction_ports2(in %a_x: i8, out a_y: i8) {
        %0 = hw.instance "simple_mixed_direction_ports_inst0" @simple_mixed_direction_ports(a_x: %a_x: i8) -> (a_y: i8)
        hw.output %0 : i8
    }
}
