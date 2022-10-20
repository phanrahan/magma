module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @aggregate_constant() -> (y: !hw.struct<x: i8, y: i4>) {
        %0 = hw.constant 0 : i8
        %1 = hw.constant 0 : i4
        %2 = hw.struct_create (%0, %1) : !hw.struct<x: i8, y: i4>
        hw.output %2 : !hw.struct<x: i8, y: i4>
    }
}
