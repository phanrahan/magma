module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @simple_aggregates_array(%a: !hw.array<8xi16>) -> (y: !hw.array<8xi16>, z: !hw.array<4xi16>) {
        %1 = hw.constant 4 : i3
        %0 = hw.array_slice %a[%1] : (!hw.array<8xi16>) -> !hw.array<4xi16>
        %3 = hw.constant 0 : i3
        %2 = hw.array_slice %a[%3] : (!hw.array<8xi16>) -> !hw.array<4xi16>
        %6 = hw.constant 0 : i2
        %5 = hw.array_get %0[%6] : !hw.array<4xi16>, i2
        %8 = hw.constant 1 : i2
        %7 = hw.array_get %0[%8] : !hw.array<4xi16>, i2
        %10 = hw.constant 2 : i2
        %9 = hw.array_get %0[%10] : !hw.array<4xi16>, i2
        %12 = hw.constant 3 : i2
        %11 = hw.array_get %0[%12] : !hw.array<4xi16>, i2
        %13 = hw.array_get %2[%6] : !hw.array<4xi16>, i2
        %14 = hw.array_get %2[%8] : !hw.array<4xi16>, i2
        %15 = hw.array_get %2[%10] : !hw.array<4xi16>, i2
        %16 = hw.array_get %2[%12] : !hw.array<4xi16>, i2
        %4 = hw.array_create %16, %15, %14, %13, %11, %9, %7, %5 : i16
        hw.output %4, %2 : !hw.array<8xi16>, !hw.array<4xi16>
    }
}
