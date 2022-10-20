module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @non_power_of_two_mux_wrapper(%a: !hw.struct<x: i8, y: i1>, %s: i4) -> (y: !hw.struct<x: i8, y: i1>) {
        %0 = hw.struct_extract %a["x"] : !hw.struct<x: i8, y: i1>
        %2 = hw.constant -1 : i8
        %1 = comb.xor %2, %0 : i8
        %3 = hw.struct_extract %a["y"] : !hw.struct<x: i8, y: i1>
        %5 = hw.constant -1 : i1
        %4 = comb.xor %5, %3 : i1
        %6 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %7 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %8 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %9 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %10 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %11 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %12 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %13 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %14 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %15 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %16 = hw.struct_create (%1, %4) : !hw.struct<x: i8, y: i1>
        %18 = hw.array_create %16, %15, %14, %13, %12, %11, %10, %9, %8, %7, %6, %a : !hw.struct<x: i8, y: i1>
        %17 = hw.array_get %18[%s] : !hw.array<12x!hw.struct<x: i8, y: i1>>, i4
        hw.output %17 : !hw.struct<x: i8, y: i1>
    }
}
