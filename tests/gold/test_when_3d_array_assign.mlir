module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_3d_array_assign(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %11 = hw.array_create %9, %8 : i2
                %12 = hw.array_create %6, %5 : i2
                %10 = hw.array_create %12, %11 : !hw.array<2xi2>
                sv.bpassign %1, %10 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %14 = hw.array_create %5, %6 : i2
                %15 = hw.array_create %8, %9 : i2
                %13 = hw.array_create %15, %14 : !hw.array<2xi2>
                sv.bpassign %1, %13 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        %2 = hw.constant 1 : i1
        %3 = hw.array_get %I[%2] : !hw.array<2x!hw.array<2xi2>>, i1
        %4 = hw.constant 0 : i1
        %5 = hw.array_get %3[%4] : !hw.array<2xi2>, i1
        %6 = hw.array_get %3[%2] : !hw.array<2xi2>, i1
        %7 = hw.array_get %I[%4] : !hw.array<2x!hw.array<2xi2>>, i1
        %8 = hw.array_get %7[%4] : !hw.array<2xi2>, i1
        %9 = hw.array_get %7[%2] : !hw.array<2xi2>, i1
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
