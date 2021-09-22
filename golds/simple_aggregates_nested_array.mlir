hw.module @simple_aggregates_nested_array(%a: !hw.array<8x!hw.array<4xi16>>) -> (%y: !hw.array<8x!hw.array<4xi16>>) {
    %9 = hw.constant 4 : i3
    %10 = hw.constant 5 : i3
    %11 = hw.constant 6 : i3
    %12 = hw.constant 7 : i3
    %13 = hw.constant 0 : i3
    %14 = hw.constant 1 : i3
    %15 = hw.constant 2 : i3
    %16 = hw.constant 3 : i3
    %0 = hw.array_get %a[%9] : !hw.array<8x!hw.array<4xi16>>
    %1 = hw.array_get %a[%10] : !hw.array<8x!hw.array<4xi16>>
    %2 = hw.array_get %a[%11] : !hw.array<8x!hw.array<4xi16>>
    %3 = hw.array_get %a[%12] : !hw.array<8x!hw.array<4xi16>>
    %4 = hw.array_get %a[%13] : !hw.array<8x!hw.array<4xi16>>
    %5 = hw.array_get %a[%14] : !hw.array<8x!hw.array<4xi16>>
    %6 = hw.array_get %a[%15] : !hw.array<8x!hw.array<4xi16>>
    %7 = hw.array_get %a[%16] : !hw.array<8x!hw.array<4xi16>>
    %8 = hw.array_create %7, %6, %5, %4, %3, %2, %1, %0 : !hw.array<4xi16>
    hw.output %8 : !hw.array<8x!hw.array<4xi16>>
}
