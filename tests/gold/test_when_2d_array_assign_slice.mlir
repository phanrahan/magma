module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign_slice(%I: !hw.array<4xi2>, %S: i1) -> (O: !hw.array<4xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<4xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<4xi2>>
        sv.alwayscomb {
            sv.if %S {
                %2 = hw.array_slice %I[%3] : (!hw.array<4xi2>) -> !hw.array<2xi2>
                %4 = hw.array_get %I[%5] : !hw.array<4xi2>, i2
                %6 = hw.array_get %I[%7] : !hw.array<4xi2>, i2
                %9 = hw.array_get %2[%10] : !hw.array<2xi2>, i1
                %11 = hw.array_get %2[%12] : !hw.array<2xi2>, i1
                %8 = hw.array_create %6, %4, %11, %9 : i2
                sv.bpassign %1, %8 : !hw.array<4xi2>
            } else {
                %13 = hw.array_slice %I[%5] : (!hw.array<4xi2>) -> !hw.array<2xi2>
                %14 = hw.array_get %I[%3] : !hw.array<4xi2>, i2
                %15 = hw.array_get %I[%16] : !hw.array<4xi2>, i2
                %18 = hw.array_get %13[%10] : !hw.array<2xi2>, i1
                %19 = hw.array_get %13[%12] : !hw.array<2xi2>, i1
                %17 = hw.array_create %15, %14, %19, %18 : i2
                sv.bpassign %1, %17 : !hw.array<4xi2>
            }
        }
        %3 = hw.constant 0 : i2
        %5 = hw.constant 2 : i2
        %7 = hw.constant 3 : i2
        %10 = hw.constant 0 : i1
        %12 = hw.constant 1 : i1
        %16 = hw.constant 1 : i2
        %20 = hw.array_slice %0[%3] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %21 = hw.array_get %0[%5] : !hw.array<4xi2>, i2
        %22 = hw.array_get %0[%7] : !hw.array<4xi2>, i2
        %24 = hw.array_get %20[%10] : !hw.array<2xi2>, i1
        %25 = hw.array_get %20[%12] : !hw.array<2xi2>, i1
        %23 = hw.array_create %22, %21, %25, %24 : i2
        hw.output %23 : !hw.array<4xi2>
    }
}
