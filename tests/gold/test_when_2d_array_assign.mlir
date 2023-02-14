module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign(%I: !hw.array<2xi2>, %S: i1) -> (O: !hw.array<2xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<2xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2xi2>>
        sv.alwayscomb {
            sv.if %S {
                %2 = hw.array_get %I[%3] : !hw.array<2xi2>, i1
                %4 = hw.array_get %I[%5] : !hw.array<2xi2>, i1
                %6 = hw.array_create %4, %2 : i2
                sv.bpassign %1, %6 : !hw.array<2xi2>
            } else {
                %7 = hw.array_get %I[%5] : !hw.array<2xi2>, i1
                %8 = hw.array_get %I[%3] : !hw.array<2xi2>, i1
                %9 = hw.array_create %8, %7 : i2
                sv.bpassign %1, %9 : !hw.array<2xi2>
            }
        }
        %3 = hw.constant 0 : i1
        %5 = hw.constant 1 : i1
        hw.output %0 : !hw.array<2xi2>
    }
}
