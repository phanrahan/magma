module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_3d_array_assign(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = hw.constant 0 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.array<2xi2>>, i1
        %3 = hw.constant 1 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
        %4 = hw.array_get %2[%1] : !hw.array<2xi2>, i1
        %5 = hw.array_get %2[%3] : !hw.array<2xi2>, i1
        %6 = hw.array_get %0[%3] : !hw.array<2xi2>, i1
        %7 = hw.array_get %0[%1] : !hw.array<2xi2>, i1
        %9 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %8 = sv.read_inout %9 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %11 = hw.array_create %5, %4 : i2
                %12 = hw.array_create %6, %7 : i2
                %10 = hw.array_create %11, %12 : !hw.array<2xi2>
                sv.bpassign %9, %10 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %14 = hw.array_create %7, %6 : i2
                %15 = hw.array_create %4, %5 : i2
                %13 = hw.array_create %14, %15 : !hw.array<2xi2>
                sv.bpassign %9, %13 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        hw.output %8 : !hw.array<2x!hw.array<2xi2>>
    }
}
