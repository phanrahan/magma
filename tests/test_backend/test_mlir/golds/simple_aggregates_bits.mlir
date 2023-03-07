module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_aggregates_bits(%a: i16) -> (y: i16, z: i8) {
        %0 = comb.extract %a from 8 : (i16) -> i8
        %1 = comb.extract %a from 0 : (i16) -> i8
        %2 = comb.concat %1, %0 : i8, i8
        hw.output %2, %1 : i16, i8
    }
}
