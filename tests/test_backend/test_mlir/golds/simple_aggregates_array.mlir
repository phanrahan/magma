module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_aggregates_array(%a: !hw.array<8xi16>) -> (y: !hw.array<8xi16>, z: !hw.array<4xi16>) {
        %1 = hw.constant 4 : i3
        %0 = hw.array_get %a[%1] : !hw.array<8xi16>, i3
        %3 = hw.constant 5 : i3
        %2 = hw.array_get %a[%3] : !hw.array<8xi16>, i3
        %5 = hw.constant 6 : i3
        %4 = hw.array_get %a[%5] : !hw.array<8xi16>, i3
        %7 = hw.constant 7 : i3
        %6 = hw.array_get %a[%7] : !hw.array<8xi16>, i3
        %9 = hw.constant 0 : i3
        %8 = hw.array_get %a[%9] : !hw.array<8xi16>, i3
        %11 = hw.constant 1 : i3
        %10 = hw.array_get %a[%11] : !hw.array<8xi16>, i3
        %13 = hw.constant 2 : i3
        %12 = hw.array_get %a[%13] : !hw.array<8xi16>, i3
        %15 = hw.constant 3 : i3
        %14 = hw.array_get %a[%15] : !hw.array<8xi16>, i3
        %16 = hw.array_create %14, %12, %10, %8, %6, %4, %2, %0 : i16
        %17 = hw.array_create %14, %12, %10, %8 : i16
        hw.output %16, %17 : !hw.array<8xi16>, !hw.array<4xi16>
    }
}
