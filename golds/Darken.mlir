hw.module @Darken(%I: i8) -> (%O: i8) {
    %0 = hw.constant 1 : i8
    %1 = comb.shl %I, %0 : i8
    hw.output %1 : i8
}
