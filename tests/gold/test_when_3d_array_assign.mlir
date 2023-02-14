module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_3d_array_assign(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
                %4 = hw.array_get %2[%5] : !hw.array<2xi2>, i1
                %6 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
                %7 = hw.array_get %6[%3] : !hw.array<2xi2>, i1
                %8 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
                %9 = hw.array_get %8[%5] : !hw.array<2xi2>, i1
                %10 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
                %11 = hw.array_get %10[%3] : !hw.array<2xi2>, i1
                %13 = hw.array_create %11, %9 : i2
                %14 = hw.array_create %7, %4 : i2
                %12 = hw.array_create %14, %13 : !hw.array<2xi2>
                sv.bpassign %1, %12 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %15 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
                %16 = hw.array_get %15[%3] : !hw.array<2xi2>, i1
                %17 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
                %18 = hw.array_get %17[%5] : !hw.array<2xi2>, i1
                %19 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
                %20 = hw.array_get %19[%3] : !hw.array<2xi2>, i1
                %21 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
                %22 = hw.array_get %21[%5] : !hw.array<2xi2>, i1
                %24 = hw.array_create %22, %20 : i2
                %25 = hw.array_create %18, %16 : i2
                %23 = hw.array_create %25, %24 : !hw.array<2xi2>
                sv.bpassign %1, %23 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        %3 = hw.constant 1 : i1
        %5 = hw.constant 0 : i1
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
