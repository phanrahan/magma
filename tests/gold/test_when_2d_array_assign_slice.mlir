module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign_slice(%I: !hw.array<4xi2>, %S: i1) -> (O: !hw.array<4xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<4xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<4xi2>>
        sv.alwayscomb {
            sv.if %S {
                %8 = hw.array_create %7, %5, %12, %10 : i2
                sv.bpassign %1, %8 : !hw.array<4xi2>
            } else {
                %17 = hw.array_create %16, %14, %19, %18 : i2
                sv.bpassign %1, %17 : !hw.array<4xi2>
            }
        }
        %2 = hw.constant 0 : i2
        %3 = hw.array_slice %I[%2] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %4 = hw.constant 2 : i2
        %5 = hw.array_get %I[%4] : !hw.array<4xi2>, i2
        %6 = hw.constant 3 : i2
        %7 = hw.array_get %I[%6] : !hw.array<4xi2>, i2
        %9 = hw.constant 0 : i1
        %10 = hw.array_get %3[%9] : !hw.array<2xi2>, i1
        %11 = hw.constant 1 : i1
        %12 = hw.array_get %3[%11] : !hw.array<2xi2>, i1
        %13 = hw.array_slice %I[%4] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %14 = hw.array_get %I[%2] : !hw.array<4xi2>, i2
        %15 = hw.constant 1 : i2
        %16 = hw.array_get %I[%15] : !hw.array<4xi2>, i2
        %18 = hw.array_get %13[%9] : !hw.array<2xi2>, i1
        %19 = hw.array_get %13[%11] : !hw.array<2xi2>, i1
        %20 = hw.array_slice %0[%2] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %21 = hw.array_get %0[%4] : !hw.array<4xi2>, i2
        %22 = hw.array_get %0[%6] : !hw.array<4xi2>, i2
        %24 = hw.array_get %20[%9] : !hw.array<2xi2>, i1
        %25 = hw.array_get %20[%11] : !hw.array<2xi2>, i1
        %23 = hw.array_create %22, %21, %25, %24 : i2
        hw.output %23 : !hw.array<4xi2>
    }
}
