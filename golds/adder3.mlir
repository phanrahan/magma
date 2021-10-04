hw.module @adder3(%I0: i16, %I1: i16, %I2: i16) -> (%O: i16) {
    %0 = comb.add %I0, %I1 : i16
    %1 = comb.add %0, %I2 : i16
    hw.output %1 : i16
}
