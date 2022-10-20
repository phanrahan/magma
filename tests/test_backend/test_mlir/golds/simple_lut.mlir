module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @LUT(%I: i2) -> (O: i8) {
        %1 = hw.constant 1 : i1
        %2 = hw.constant 0 : i1
        %3 = hw.array_create %1, %2, %1, %2 : i1
        %0 = hw.array_get %3[%I] : !hw.array<4xi1>, i2
        %5 = hw.array_create %1, %1, %2, %1 : i1
        %4 = hw.array_get %5[%I] : !hw.array<4xi1>, i2
        %7 = hw.array_create %1, %1, %1, %1 : i1
        %6 = hw.array_get %7[%I] : !hw.array<4xi1>, i2
        %9 = hw.array_create %1, %1, %1, %1 : i1
        %8 = hw.array_get %9[%I] : !hw.array<4xi1>, i2
        %11 = hw.array_create %2, %1, %2, %1 : i1
        %10 = hw.array_get %11[%I] : !hw.array<4xi1>, i2
        %13 = hw.array_create %1, %1, %1, %2 : i1
        %12 = hw.array_get %13[%I] : !hw.array<4xi1>, i2
        %15 = hw.array_create %1, %2, %2, %1 : i1
        %14 = hw.array_get %15[%I] : !hw.array<4xi1>, i2
        %17 = hw.array_create %1, %1, %1, %1 : i1
        %16 = hw.array_get %17[%I] : !hw.array<4xi1>, i2
        %18 = comb.concat %16, %14, %12, %10, %8, %6, %4, %0 : i1, i1, i1, i1, i1, i1, i1, i1
        hw.output %18 : i8
    }
    hw.module @simple_lut(%a: i2) -> (y: i8) {
        %0 = hw.instance "LUT_inst0" @LUT(I: %a: i2) -> (O: i8)
        hw.output %0 : i8
    }
}
