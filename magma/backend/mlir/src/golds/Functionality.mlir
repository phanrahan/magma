hw.module @clb(%a: i16, %b: i16, %c: i16, %d: i16) -> (O: i16) {
    %0 = comb.and %a, %b : i16
    %2 = hw.constant -1 : i16
    %1 = comb.xor %2, %c : i16
    %3 = comb.and %1, %d : i16
    %4 = comb.or %0, %3 : i16
    hw.output %4 : i16
}
hw.module @Functionality(%x: i16, %y: i16) -> (z: i16) {
    %0 = hw.instance "clb_inst0" @clb(a: %x: i16, b: %y: i16, c: %x: i16, d: %y: i16) -> (O: i16)
    hw.output %0 : i16
}
