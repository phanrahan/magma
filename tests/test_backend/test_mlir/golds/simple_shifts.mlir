module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_shifts(%I00: i8, %I01: i8, %I10: i8, %I11: i8, %I20: i8, %I21: i8) -> (O0: i8, O1: i8, O2: i8) {
        %0 = comb.shl %I00, %I01 : i8
        %1 = comb.shru %I10, %I11 : i8
        %2 = comb.shrs %I20, %I21 : i8
        hw.output %0, %1, %2 : i8, i8, i8
    }
}
