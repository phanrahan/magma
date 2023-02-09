module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_array_3d_bulk_child(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = hw.constant 0 : i1
        %0 = hw.array_get %I[%1] : !hw.array<2x!hw.array<2xi2>>, i1
        %3 = hw.constant 1 : i1
        %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
        %5 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %4 = sv.read_inout %5 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %6 = hw.array_create %2, %0 : !hw.array<2xi2>
                sv.bpassign %5, %6 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %7 = hw.array_create %0, %2 : !hw.array<2xi2>
                sv.bpassign %5, %7 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        hw.output %4 : !hw.array<2x!hw.array<2xi2>>
    }
}
