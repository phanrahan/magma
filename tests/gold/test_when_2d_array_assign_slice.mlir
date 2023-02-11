module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_2d_array_assign_slice(%I: !hw.array<4xi2>, %S: i1) -> (O: !hw.array<4xi2>) {
        %1 = sv.reg : !hw.inout<!hw.array<4xi2>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<4xi2>>
        sv.alwayscomb {
            sv.if %S {
                %3 = hw.constant 0 : i2
                %2 = hw.array_slice %I[%3] : (!hw.array<4xi2>) -> !hw.array<2xi2>
                %5 = hw.constant 2 : i2
                %4 = hw.array_get %I[%5] : !hw.array<4xi2>, i2
                %7 = hw.constant 3 : i2
                %6 = hw.array_get %I[%7] : !hw.array<4xi2>, i2
                %10 = hw.constant 0 : i1
                %9 = hw.array_get %2[%10] : !hw.array<2xi2>, i1
                %12 = hw.constant 1 : i1
                %11 = hw.array_get %2[%12] : !hw.array<2xi2>, i1
                %8 = hw.array_create %6, %4, %11, %9 : i2
                sv.bpassign %1, %8 : !hw.array<4xi2>
            } else {
                %14 = hw.constant 2 : i2
                %13 = hw.array_slice %I[%14] : (!hw.array<4xi2>) -> !hw.array<2xi2>
                %16 = hw.constant 0 : i2
                %15 = hw.array_get %I[%16] : !hw.array<4xi2>, i2
                %18 = hw.constant 1 : i2
                %17 = hw.array_get %I[%18] : !hw.array<4xi2>, i2
                %21 = hw.constant 0 : i1
                %20 = hw.array_get %13[%21] : !hw.array<2xi2>, i1
                %23 = hw.constant 1 : i1
                %22 = hw.array_get %13[%23] : !hw.array<2xi2>, i1
                %19 = hw.array_create %17, %15, %22, %20 : i2
                sv.bpassign %1, %19 : !hw.array<4xi2>
            }
        }
        %25 = hw.constant 0 : i2
        %24 = hw.array_slice %0[%25] : (!hw.array<4xi2>) -> !hw.array<2xi2>
        %27 = hw.constant 2 : i2
        %26 = hw.array_get %0[%27] : !hw.array<4xi2>, i2
        %29 = hw.constant 3 : i2
        %28 = hw.array_get %0[%29] : !hw.array<4xi2>, i2
        %32 = hw.constant 0 : i1
        %31 = hw.array_get %24[%32] : !hw.array<2xi2>, i1
        %34 = hw.constant 1 : i1
        %33 = hw.array_get %24[%34] : !hw.array<2xi2>, i1
        %30 = hw.array_create %28, %26, %33, %31 : i2
        hw.output %30 : !hw.array<4xi2>
    }
}
