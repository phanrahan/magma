hw.module @simple_aggregates_tuple(%a: !hw.struct<x: i8, y: i8>) -> (%y: !hw.struct<x: i8, y: i8>) {
    %5 = hw.constant -1 : i8
    %6 = hw.constant -1 : i8
    %0 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i8>
    %1 = hw.struct_extract %a["y"] : !hw.struct<x: i8, y: i8>
    %2 = comb.xor %0, %5 : i8
    %3 = comb.xor %1, %6 : i8
    %4 = hw.struct_create (%2, %3) : !hw.struct<x: i8, y: i8>
    hw.output %4 : !hw.struct<x: i8, y: i8>
}
