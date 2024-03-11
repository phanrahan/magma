module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_mixed_direction_ports(in %a_x: i8, out a_y: i8) {
        hw.output %a_x : i8
    }
}
