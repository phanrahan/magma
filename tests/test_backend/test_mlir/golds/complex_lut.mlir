hw.module @LUT(%I: i2) -> (O: !hw.array<2x!hw.struct<x: i8, y: i1>>) {
    %1 = hw.constant 0 : i1
    %2 = hw.constant 1 : i1
    %3 = hw.array_create %1, %2, %2, %2 : i1
    %0 = hw.array_get %3[%I] : !hw.array<4xi1>
    %4 = comb.concat %0 : i1
    %6 = hw.array_create %2, %2, %2, %2 : i1
    %5 = hw.array_get %6[%I] : !hw.array<4xi1>
    %7 = comb.concat %5 : i1
    %9 = hw.array_create %2, %1, %2, %2 : i1
    %8 = hw.array_get %9[%I] : !hw.array<4xi1>
    %10 = comb.concat %8 : i1
    %12 = hw.array_create %2, %2, %2, %2 : i1
    %11 = hw.array_get %12[%I] : !hw.array<4xi1>
    %13 = comb.concat %11 : i1
    %15 = hw.array_create %2, %1, %1, %1 : i1
    %14 = hw.array_get %15[%I] : !hw.array<4xi1>
    %16 = comb.concat %14 : i1
    %18 = hw.array_create %1, %1, %2, %1 : i1
    %17 = hw.array_get %18[%I] : !hw.array<4xi1>
    %19 = comb.concat %17 : i1
    %21 = hw.array_create %1, %2, %2, %1 : i1
    %20 = hw.array_get %21[%I] : !hw.array<4xi1>
    %22 = comb.concat %20 : i1
    %24 = hw.array_create %1, %1, %1, %1 : i1
    %23 = hw.array_get %24[%I] : !hw.array<4xi1>
    %25 = comb.concat %23 : i1
    %26 = hw.array_concat %25, %22, %19, %16, %13, %10, %7, %4 : i1, i1, i1, i1, i1, i1, i1, i1
    %28 = hw.array_create %2, %2, %2, %1 : i1
    %27 = hw.array_get %28[%I] : !hw.array<4xi1>
    %29 = hw.struct_create (%26, %27) : !hw.struct<x: i8, y: i1>
    %30 = hw.array_create %29 : !hw.struct<x: i8, y: i1>
    %32 = hw.array_create %1, %2, %2, %2 : i1
    %31 = hw.array_get %32[%I] : !hw.array<4xi1>
    %33 = comb.concat %31 : i1
    %35 = hw.array_create %2, %1, %2, %2 : i1
    %34 = hw.array_get %35[%I] : !hw.array<4xi1>
    %36 = comb.concat %34 : i1
    %38 = hw.array_create %1, %1, %1, %1 : i1
    %37 = hw.array_get %38[%I] : !hw.array<4xi1>
    %39 = comb.concat %37 : i1
    %41 = hw.array_create %1, %2, %1, %2 : i1
    %40 = hw.array_get %41[%I] : !hw.array<4xi1>
    %42 = comb.concat %40 : i1
    %44 = hw.array_create %2, %1, %1, %1 : i1
    %43 = hw.array_get %44[%I] : !hw.array<4xi1>
    %45 = comb.concat %43 : i1
    %47 = hw.array_create %1, %1, %1, %1 : i1
    %46 = hw.array_get %47[%I] : !hw.array<4xi1>
    %48 = comb.concat %46 : i1
    %50 = hw.array_create %1, %2, %2, %1 : i1
    %49 = hw.array_get %50[%I] : !hw.array<4xi1>
    %51 = comb.concat %49 : i1
    %53 = hw.array_create %1, %2, %2, %2 : i1
    %52 = hw.array_get %53[%I] : !hw.array<4xi1>
    %54 = comb.concat %52 : i1
    %55 = hw.array_concat %54, %51, %48, %45, %42, %39, %36, %33 : i1, i1, i1, i1, i1, i1, i1, i1
    %57 = hw.array_create %2, %2, %1, %1 : i1
    %56 = hw.array_get %57[%I] : !hw.array<4xi1>
    %58 = hw.struct_create (%55, %56) : !hw.struct<x: i8, y: i1>
    %59 = hw.array_create %58 : !hw.struct<x: i8, y: i1>
    %60 = hw.array_concat %59, %30 : !hw.array<1x!hw.struct<x: i8, y: i1>>, !hw.array<1x!hw.struct<x: i8, y: i1>>
    hw.output %60 : !hw.array<2x!hw.struct<x: i8, y: i1>>
}
hw.module @complex_lut(%a: i2) -> (y: !hw.array<2x!hw.struct<x: i8, y: i1>>) {
    %0 = hw.instance "LUT_inst0" @LUT(I: %a: i2) -> (O: !hw.array<2x!hw.struct<x: i8, y: i1>>)
    hw.output %0 : !hw.array<2x!hw.struct<x: i8, y: i1>>
}
