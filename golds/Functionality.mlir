hw.module @clb(%a: i16, %b: i16, %c: i16, %d: i16) -> (%O: i16) {
    %0 = hw.constant -1 : i16
    %1 = comb.and %a, %b : i16
    %2 = comb.xor %c, %0 : i16
    %3 = comb.and %2, %d : i16
    %4 = comb.or %1, %3 : i16
    hw.output %4 : i16
}
hw.module @Functionality(%x: i16, %y: i16) -> (%z: i16) {
    %0 = hw.instance "clb_inst0" @clb(%x, %y, %x, %y) : (i16, i16, i16, i16) -> (i16)
    hw.output %0 : i16
}
