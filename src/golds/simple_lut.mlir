hw.module @LUT(%I: i2) -> (%O: i8) {
    %1 = hw.constant 0 : i1
    %2 = hw.constant 1 : i1
    %3 = hw.constant 0 : i1
    %4 = hw.constant 1 : i1
    %5 = hw.array_create %1, %2, %3, %4 : i1
    %0 = hw.array_get %5[%I] : !hw.array<4xi1>
    %7 = hw.constant 1 : i1
    %8 = hw.constant 0 : i1
    %9 = hw.constant 1 : i1
    %10 = hw.constant 1 : i1
    %11 = hw.array_create %7, %8, %9, %10 : i1
    %6 = hw.array_get %11[%I] : !hw.array<4xi1>
    %13 = hw.constant 1 : i1
    %14 = hw.constant 1 : i1
    %15 = hw.constant 1 : i1
    %16 = hw.constant 1 : i1
    %17 = hw.array_create %13, %14, %15, %16 : i1
    %12 = hw.array_get %17[%I] : !hw.array<4xi1>
    %19 = hw.constant 1 : i1
    %20 = hw.constant 1 : i1
    %21 = hw.constant 1 : i1
    %22 = hw.constant 1 : i1
    %23 = hw.array_create %19, %20, %21, %22 : i1
    %18 = hw.array_get %23[%I] : !hw.array<4xi1>
    %25 = hw.constant 1 : i1
    %26 = hw.constant 0 : i1
    %27 = hw.constant 1 : i1
    %28 = hw.constant 0 : i1
    %29 = hw.array_create %25, %26, %27, %28 : i1
    %24 = hw.array_get %29[%I] : !hw.array<4xi1>
    %31 = hw.constant 0 : i1
    %32 = hw.constant 1 : i1
    %33 = hw.constant 1 : i1
    %34 = hw.constant 1 : i1
    %35 = hw.array_create %31, %32, %33, %34 : i1
    %30 = hw.array_get %35[%I] : !hw.array<4xi1>
    %37 = hw.constant 1 : i1
    %38 = hw.constant 0 : i1
    %39 = hw.constant 0 : i1
    %40 = hw.constant 1 : i1
    %41 = hw.array_create %37, %38, %39, %40 : i1
    %36 = hw.array_get %41[%I] : !hw.array<4xi1>
    %43 = hw.constant 1 : i1
    %44 = hw.constant 1 : i1
    %45 = hw.constant 1 : i1
    %46 = hw.constant 1 : i1
    %47 = hw.array_create %43, %44, %45, %46 : i1
    %42 = hw.array_get %47[%I] : !hw.array<4xi1>
    %48 = comb.concat %42, %36, %30, %24, %18, %12, %6, %0 : (i1, i1, i1, i1, i1, i1, i1, i1) -> (i8)
    hw.output %48 : i8
}
hw.module @simple_lut(%a: i2) -> (%y: i8) {
    %0 = hw.instance "LUT_inst0" @LUT(%a) : (i2) -> (i8)
    hw.output %0 : i8
}
