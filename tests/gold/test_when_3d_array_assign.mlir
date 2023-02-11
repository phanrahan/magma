module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_3d_array_assign(%I: !hw.array<2x!hw.array<2xi2>>, %S: i1) -> (O: !hw.array<2x!hw.array<2xi2>>) {
        %1 = sv.reg : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        %0 = sv.read_inout %1 : !hw.inout<!hw.array<2x!hw.array<2xi2>>>
        sv.alwayscomb {
            sv.if %S {
                %3 = hw.constant 1 : i1
                %2 = hw.array_get %I[%3] : !hw.array<2x!hw.array<2xi2>>, i1
                %5 = hw.constant 0 : i1
                %4 = hw.array_get %2[%5] : !hw.array<2xi2>, i1
                %7 = hw.constant 1 : i1
                %6 = hw.array_get %I[%7] : !hw.array<2x!hw.array<2xi2>>, i1
                %9 = hw.constant 1 : i1
                %8 = hw.array_get %6[%9] : !hw.array<2xi2>, i1
                %11 = hw.constant 0 : i1
                %10 = hw.array_get %I[%11] : !hw.array<2x!hw.array<2xi2>>, i1
                %13 = hw.constant 0 : i1
                %12 = hw.array_get %10[%13] : !hw.array<2xi2>, i1
                %15 = hw.constant 0 : i1
                %14 = hw.array_get %I[%15] : !hw.array<2x!hw.array<2xi2>>, i1
                %17 = hw.constant 1 : i1
                %16 = hw.array_get %14[%17] : !hw.array<2xi2>, i1
                %19 = hw.array_create %8, %4 : i2
                %20 = hw.array_create %16, %12 : i2
                %18 = hw.array_create %19, %20 : !hw.array<2xi2>
                sv.bpassign %1, %18 : !hw.array<2x!hw.array<2xi2>>
            } else {
                %22 = hw.constant 0 : i1
                %21 = hw.array_get %I[%22] : !hw.array<2x!hw.array<2xi2>>, i1
                %24 = hw.constant 1 : i1
                %23 = hw.array_get %21[%24] : !hw.array<2xi2>, i1
                %26 = hw.constant 0 : i1
                %25 = hw.array_get %I[%26] : !hw.array<2x!hw.array<2xi2>>, i1
                %28 = hw.constant 0 : i1
                %27 = hw.array_get %25[%28] : !hw.array<2xi2>, i1
                %30 = hw.constant 1 : i1
                %29 = hw.array_get %I[%30] : !hw.array<2x!hw.array<2xi2>>, i1
                %32 = hw.constant 1 : i1
                %31 = hw.array_get %29[%32] : !hw.array<2xi2>, i1
                %34 = hw.constant 1 : i1
                %33 = hw.array_get %I[%34] : !hw.array<2x!hw.array<2xi2>>, i1
                %36 = hw.constant 0 : i1
                %35 = hw.array_get %33[%36] : !hw.array<2xi2>, i1
                %38 = hw.array_create %27, %23 : i2
                %39 = hw.array_create %35, %31 : i2
                %37 = hw.array_create %38, %39 : !hw.array<2xi2>
                sv.bpassign %1, %37 : !hw.array<2x!hw.array<2xi2>>
            }
        }
        hw.output %0 : !hw.array<2x!hw.array<2xi2>>
    }
}
