module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_array_3d_bulk_child(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %3 = hw.constant 0 : i1
                %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
                %5 = hw.constant 1 : i1
                %4 = hw.array_get %I[%5] : !hw.array<2x!hw.array<2xi2>>, i1
                %6 = hw.array_create %4, %2 : !hw.array<2xi2>
                sv.bpassign %1, %6 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %8 = hw.constant 0 : i1
                %7 = hw.array_get %I[%8] : !hw.array<2x!hw.array<2xi2>>, i1
                %10 = hw.constant 1 : i1
                %9 = hw.array_get %I[%10] : !hw.array<2x!hw.array<2xi2>>, i1
                %11 = hw.array_create %7, %9 : !hw.array<2xi2>
                sv.bpassign %1, %11 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
