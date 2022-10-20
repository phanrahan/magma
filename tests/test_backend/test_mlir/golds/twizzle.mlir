module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @twizzler(%I0: i1, %I1: i1, %I2: i1) -> (O0: i1, O1: i1, O2: i1) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %I1 : i1
        %2 = comb.xor %1, %I0 : i1
        %3 = comb.xor %1, %I2 : i1
        hw.output %0, %2, %3 : i1, i1, i1
    }
    hw.module @twizzle(%I: i1) -> (O: i1) {
        %2, %3, %4 = hw.instance "t0" @twizzler(I0: %I: i1, I1: %0: i1, I2: %1: i1) -> (O0: i1, O1: i1, O2: i1)
        %0, %1, %5 = hw.instance "t1" @twizzler(I0: %2: i1, I1: %3: i1, I2: %4: i1) -> (O0: i1, O1: i1, O2: i1)
        hw.output %5 : i1
    }
}
