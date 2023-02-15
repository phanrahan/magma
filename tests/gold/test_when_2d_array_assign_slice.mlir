module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign_slice(%I: !hw.array<4xi2>, %S: i1) -> (O: !hw.array<4xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<4xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<4xi2>>
        sv.alwayscomb {
            sv.if %S {
                %9 = hw.array_create %7, %5 : i2
                %8 = hw.array_concat %9, %3 : !hw.array<2xi2>, !hw.array<2xi2>
                sv.bpassign %1, %8 : !hw.array<4xi2>
            } else {
                %15 = hw.array_create %13, %11 : i2
                %14 = hw.array_concat %15, %10 : !hw.array<2xi2>, !hw.array<2xi2>
                sv.bpassign %1, %14 : !hw.array<4xi2>
            }
        }
        %2 = hw.constant 0 : i2
        %3 = hw.array_slice %I[%2] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %4 = hw.constant 2 : i2
        %5 = hw.array_get %I[%4] : !hw.array<4xi2>, i2
        %6 = hw.constant 3 : i2
        %7 = hw.array_get %I[%6] : !hw.array<4xi2>, i2
        %10 = hw.array_slice %I[%4] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %11 = hw.array_get %I[%2] : !hw.array<4xi2>, i2
        %12 = hw.constant 1 : i2
        %13 = hw.array_get %I[%12] : !hw.array<4xi2>, i2
        %16 = hw.array_slice %0[%2] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %17 = hw.array_get %0[%4] : !hw.array<4xi2>, i2
        %18 = hw.array_get %0[%6] : !hw.array<4xi2>, i2
        %20 = hw.array_create %17, %18 : i2
        %19 = hw.array_concat %16, %20 : !hw.array<2xi2>, !hw.array<2xi2>
        hw.output %19 : !hw.array<4xi2>
    }
}
