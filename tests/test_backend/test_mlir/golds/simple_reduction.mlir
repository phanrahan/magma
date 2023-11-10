module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_reduction(in %I0: i8, in %I1: i8, in %I2: i8, out O0: i1, out O1: i1, out O2: i1) {
        %1 = hw.constant -1 : i8
        %0 = comb.icmp eq %I0, %1 : i8
        %3 = hw.constant 0 : i8
        %2 = comb.icmp ne %I1, %3 : i8
        %4 = comb.parity %I2 : i8
        hw.output %0, %2, %4 : i1, i1, i1
    }
}
