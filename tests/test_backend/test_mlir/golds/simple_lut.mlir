hw.module @LUT(%I: i2) -> (O: i8) {
    %1 = hw.constant 1 : i1
    %2 = hw.constant 0 : i1
    %3 = hw.array_create %1, %2, %1, %2 : i1
    %0 = hw.array_get %3[%I] : !hw.array<4xi1>
    %4 = comb.concat %0 : i1
    %6 = hw.array_create %1, %1, %2, %1 : i1
    %5 = hw.array_get %6[%I] : !hw.array<4xi1>
    %7 = comb.concat %5 : i1
    %9 = hw.array_create %1, %1, %1, %1 : i1
    %8 = hw.array_get %9[%I] : !hw.array<4xi1>
    %10 = comb.concat %8 : i1
    %12 = hw.array_create %1, %1, %1, %1 : i1
    %11 = hw.array_get %12[%I] : !hw.array<4xi1>
    %13 = comb.concat %11 : i1
    %15 = hw.array_create %2, %1, %2, %1 : i1
    %14 = hw.array_get %15[%I] : !hw.array<4xi1>
    %16 = comb.concat %14 : i1
    %18 = hw.array_create %1, %1, %1, %2 : i1
    %17 = hw.array_get %18[%I] : !hw.array<4xi1>
    %19 = comb.concat %17 : i1
    %21 = hw.array_create %1, %2, %2, %1 : i1
    %20 = hw.array_get %21[%I] : !hw.array<4xi1>
    %22 = comb.concat %20 : i1
    %24 = hw.array_create %1, %1, %1, %1 : i1
    %23 = hw.array_get %24[%I] : !hw.array<4xi1>
    %25 = comb.concat %23 : i1
    %26 = hw.array_concat %25, %22, %19, %16, %13, %10, %7, %4 : i1, i1, i1, i1, i1, i1, i1, i1
    hw.output %26 : i8
}
hw.module @simple_lut(%a: i2) -> (y: i8) {
    %0 = hw.instance "LUT_inst0" @LUT(I: %a: i2) -> (O: i8)
    hw.output %0 : i8
}
