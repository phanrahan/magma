hw.module @simple_aggregates_nested_array(%a: !hw.array<8x!hw.array<4xi16>>) -> (y: !hw.array<8x!hw.array<4xi16>>) {
    %1 = hw.constant 4 : i3
    %0 = hw.array_slice %a at %1 : (!hw.array<8x!hw.array<4xi16>>) -> !hw.array<4x!hw.array<4xi16>>
    %3 = hw.constant 0 : i3
    %2 = hw.array_slice %a at %3 : (!hw.array<8x!hw.array<4xi16>>) -> !hw.array<4x!hw.array<4xi16>>
    %4 = hw.array_concat %2, %0 : !hw.array<4x!hw.array<4xi16>>, !hw.array<4x!hw.array<4xi16>>
    hw.output %4 : !hw.array<8x!hw.array<4xi16>>
}
