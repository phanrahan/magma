module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_shifts(in %I00: i8, in %I01: i8, in %I10: i8, in %I11: i8, in %I20: i8, in %I21: i8, out O0: i8, out O1: i8, out O2: i8) {
        %0 = comb.shl %I00, %I01 : i8
        %1 = comb.shru %I10, %I11 : i8
        %2 = comb.shrs %I20, %I21 : i8
        hw.output %0, %1, %2 : i8, i8, i8
    }
}
