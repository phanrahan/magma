hw.module @comb(%a: i16, %b: i16, %c: i16) -> (%y: i16, %z: i16) {
    %3 = hw.constant -1 : i16
    %0 = comb.xor %a, %3 : i16
    %1 = comb.or %a, %0 : i16
    %2 = comb.or %1, %b : i16
    hw.output %2, %2 : i16, i16
}
hw.module @simple_hierarchy(%a: i16, %b: i16, %c: i16) -> (%y: i16, %z: i16) {
    %0, %1 = hw.instance "comb_inst0" @comb(%a, %b, %c) : (i16, i16, i16) -> (i16, i16)
    hw.output %0, %1 : i16, i16
}
