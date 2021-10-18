hw.module @_Foo(%_Foo_a_x: i8) -> (%_Foo_a_y: i8) {
    hw.output %_Foo_a_x : i8
}
hw.module @complex_mixed_direction_ports(%complex_mixed_direction_ports_a_x: i8) -> (%complex_mixed_direction_ports_a_y: i8) {
    %0 = hw.instance "_Foo_inst0" @_Foo(%complex_mixed_direction_ports_a_x) : (i8) -> (i8)
    hw.output %0 : i8
}
