hw.module @comb(%a: i16, %b: i16, %c: i16) -> (%y: i16, %z: i16) {
    %0 = hw.constant -1 : i16
    %1 = comb.xor %a, %0 : i16
    %2 = comb.or %a, %1 : i16
    %3 = comb.or %2, %b : i16
    hw.output %3, %3 : i16, i16
}
hw.module @simple_hierarchy(%a: i16, %b: i16, %c: i16) -> (%y: i16, %z: i16) {
    %0, %1 = hw.instance "comb_inst0" @comb(%a, %b, %c) : (i16, i16, i16) -> (i16, i16)
    hw.output %0, %1 : i16, i16
}
