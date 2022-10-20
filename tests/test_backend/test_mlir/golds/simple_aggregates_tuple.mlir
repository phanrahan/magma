module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_aggregates_tuple(%a: !hw.struct<0: i8, 1: i8>) -> (y: !hw.struct<0: i8, 1: i8>) {
        %0 = hw.struct_extract %a["0"] : !hw.struct<0: i8, 1: i8>
        %2 = hw.constant -1 : i8
        %1 = comb.xor %2, %0 : i8
        %3 = hw.struct_extract %a["1"] : !hw.struct<0: i8, 1: i8>
        %4 = comb.xor %2, %3 : i8
        %5 = hw.struct_create (%1, %4) : !hw.struct<0: i8, 1: i8>
        hw.output %5 : !hw.struct<0: i8, 1: i8>
    }
}
