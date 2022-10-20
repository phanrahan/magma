module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @LUT(%I: i2) -> (O: !hw.array<2x!hw.struct<x: i8, y: i1>>) {
        %1 = hw.constant 0 : i1
        %2 = hw.constant 1 : i1
        %3 = hw.array_create %1, %2, %2, %2 : i1
        %0 = hw.array_get %3[%I] : !hw.array<4xi1>, i2
        %5 = hw.array_create %2, %2, %2, %2 : i1
        %4 = hw.array_get %5[%I] : !hw.array<4xi1>, i2
        %7 = hw.array_create %2, %1, %2, %2 : i1
        %6 = hw.array_get %7[%I] : !hw.array<4xi1>, i2
        %9 = hw.array_create %2, %2, %2, %2 : i1
        %8 = hw.array_get %9[%I] : !hw.array<4xi1>, i2
        %11 = hw.array_create %2, %1, %1, %1 : i1
        %10 = hw.array_get %11[%I] : !hw.array<4xi1>, i2
        %13 = hw.array_create %1, %1, %2, %1 : i1
        %12 = hw.array_get %13[%I] : !hw.array<4xi1>, i2
        %15 = hw.array_create %1, %2, %2, %1 : i1
        %14 = hw.array_get %15[%I] : !hw.array<4xi1>, i2
        %17 = hw.array_create %1, %1, %1, %1 : i1
        %16 = hw.array_get %17[%I] : !hw.array<4xi1>, i2
        %18 = comb.concat %16, %14, %12, %10, %8, %6, %4, %0 : i1, i1, i1, i1, i1, i1, i1, i1
        %20 = hw.array_create %2, %2, %2, %1 : i1
        %19 = hw.array_get %20[%I] : !hw.array<4xi1>, i2
        %21 = hw.struct_create (%18, %19) : !hw.struct<x: i8, y: i1>
        %23 = hw.array_create %1, %2, %2, %2 : i1
        %22 = hw.array_get %23[%I] : !hw.array<4xi1>, i2
        %25 = hw.array_create %2, %1, %2, %2 : i1
        %24 = hw.array_get %25[%I] : !hw.array<4xi1>, i2
        %27 = hw.array_create %1, %1, %1, %1 : i1
        %26 = hw.array_get %27[%I] : !hw.array<4xi1>, i2
        %29 = hw.array_create %1, %2, %1, %2 : i1
        %28 = hw.array_get %29[%I] : !hw.array<4xi1>, i2
        %31 = hw.array_create %2, %1, %1, %1 : i1
        %30 = hw.array_get %31[%I] : !hw.array<4xi1>, i2
        %33 = hw.array_create %1, %1, %1, %1 : i1
        %32 = hw.array_get %33[%I] : !hw.array<4xi1>, i2
        %35 = hw.array_create %1, %2, %2, %1 : i1
        %34 = hw.array_get %35[%I] : !hw.array<4xi1>, i2
        %37 = hw.array_create %1, %2, %2, %2 : i1
        %36 = hw.array_get %37[%I] : !hw.array<4xi1>, i2
        %38 = comb.concat %36, %34, %32, %30, %28, %26, %24, %22 : i1, i1, i1, i1, i1, i1, i1, i1
        %40 = hw.array_create %2, %2, %1, %1 : i1
        %39 = hw.array_get %40[%I] : !hw.array<4xi1>, i2
        %41 = hw.struct_create (%38, %39) : !hw.struct<x: i8, y: i1>
        %42 = hw.array_create %41, %21 : !hw.struct<x: i8, y: i1>
        hw.output %42 : !hw.array<2x!hw.struct<x: i8, y: i1>>
    }
    hw.module @complex_lut(%a: i2) -> (y: !hw.array<2x!hw.struct<x: i8, y: i1>>) {
        %0 = hw.instance "LUT_inst0" @LUT(I: %a: i2) -> (O: !hw.array<2x!hw.struct<x: i8, y: i1>>)
        hw.output %0 : !hw.array<2x!hw.struct<x: i8, y: i1>>
    }
}
