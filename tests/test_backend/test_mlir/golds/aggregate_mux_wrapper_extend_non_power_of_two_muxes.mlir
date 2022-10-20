module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @aggregate_mux_wrapper(%a: !hw.struct<x: i8, y: i1>, %s: i1) -> (y: !hw.struct<x: i8, y: i1>) {
        %0 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
        %2 = hw.constant -1 : i8
        %1 = comb.xor %2, %0 : i8
        %3 = hw.struct_extract %a["y"] : !hw.struct<x: i8, y: i1>
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %3 : i1
        %6 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %8 = hw.array_create %6, %a : !hw.struct<x: i8, y: i1>
        %7 = hw.array_get %8[%s] : !hw.array<2x!hw.struct<x: i8, y: i1>>, i1
        hw.output %7 : !hw.struct<x: i8, y: i1>
    }
}
