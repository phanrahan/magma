module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
        %0 = hw.constant 0 : i2
        %1 = hw.constant 1 : i2
        %2 = hw.constant 1 : i2
        %3 = hw.constant 0 : i2
        %4 = hw.constant 0 : i1
        %5 = hw.constant 1 : i1
        %12 = sv.reg : !hw.inout<i2>
        %6 = sv.read_inout %12 : !hw.inout<i2>
        %13 = sv.reg : !hw.inout<i2>
        %7 = sv.read_inout %13 : !hw.inout<i2>
        %14 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %14 : !hw.inout<i1>
        %15 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %15 : !hw.inout<i1>
        %16 = sv.reg : !hw.inout<i1>
        %10 = sv.read_inout %16 : !hw.inout<i1>
        %17 = sv.reg : !hw.inout<i1>
        %11 = sv.read_inout %17 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %14, %4 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %5 : i1
                sv.bpassign %17, %4 : i1
            } else {
                sv.bpassign %14, %5 : i1
                sv.bpassign %15, %4 : i1
                sv.bpassign %16, %4 : i1
                sv.bpassign %17, %4 : i1
            }
        }
        %18 = comb.concat %11, %10, %9, %8 : i1, i1, i1, i1
        %20 = sv.wire sym @test_when_lazy_array_slice.x {name="x"} : !hw.inout<i4>
        sv.assign %20, %18 : i4
        %19 = sv.read_inout %20 : !hw.inout<i4>
        hw.output %19 : i4
    }
}
