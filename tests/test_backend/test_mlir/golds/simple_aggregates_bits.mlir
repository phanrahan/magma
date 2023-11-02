module attributes {circt.loweringOptions = "locationInfoStyle=none,omitVersionComment"} {
    hw.module @simple_aggregates_bits(in %a: i16, out y: i16, out z: i8) {
        %0 = comb.extract %a from 8 : (i16) -> i8
        %1 = comb.extract %a from 0 : (i16) -> i8
        %2 = comb.concat %1, %0 : i8, i8
        hw.output %2, %1 : i16, i8
    }
}
