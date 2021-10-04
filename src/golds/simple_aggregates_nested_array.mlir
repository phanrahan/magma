hw.module @simple_aggregates_nested_array(%a: !hw.array<8x!hw.array<4xi16>>) -> (%y: !hw.array<8x!hw.array<4xi16>>) {
    %0 = hw.constant 4 : i3
    %1 = hw.constant 5 : i3
    %2 = hw.constant 6 : i3
    %3 = hw.constant 7 : i3
    %4 = hw.constant 0 : i3
    %5 = hw.constant 1 : i3
    %6 = hw.constant 2 : i3
    %7 = hw.constant 3 : i3
    %8 = hw.array_get %a[%0] : !hw.array<8x!hw.array<4xi16>>
    %9 = hw.array_get %a[%1] : !hw.array<8x!hw.array<4xi16>>
    %10 = hw.array_get %a[%2] : !hw.array<8x!hw.array<4xi16>>
    %11 = hw.array_get %a[%3] : !hw.array<8x!hw.array<4xi16>>
    %12 = hw.array_get %a[%4] : !hw.array<8x!hw.array<4xi16>>
    %13 = hw.array_get %a[%5] : !hw.array<8x!hw.array<4xi16>>
    %14 = hw.array_get %a[%6] : !hw.array<8x!hw.array<4xi16>>
    %15 = hw.array_get %a[%7] : !hw.array<8x!hw.array<4xi16>>
    %16 = hw.array_create %15, %14, %13, %12, %11, %10, %9, %8 : !hw.array<4xi16>
    hw.output %16 : !hw.array<8x!hw.array<4xi16>>
}
