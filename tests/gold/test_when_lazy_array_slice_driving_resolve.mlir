module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_driving_resolve(%S: i1) -> (O: i4) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 2 : i4
        %2 = hw.constant 4 : i4
        %3 = hw.constant 0 : i1
        %4 = hw.constant 1 : i1
        %10 = sv.reg : !hw.inout<i4>
        %5 = sv.read_inout %10 : !hw.inout<i4>
        %11 = sv.reg : !hw.inout<i1>
        %6 = sv.read_inout %11 : !hw.inout<i1>
        %12 = sv.reg : !hw.inout<i1>
        %7 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %13 : !hw.inout<i1>
        %14 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %14 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %11, %3 : i1
                sv.bpassign %12, %4 : i1
                sv.bpassign %13, %3 : i1
                sv.bpassign %14, %3 : i1
            } else {
                sv.bpassign %11, %3 : i1
                sv.bpassign %12, %3 : i1
                sv.bpassign %13, %4 : i1
                sv.bpassign %14, %3 : i1
            }
        }
        %15 = comb.concat %9, %8, %7, %0 : i1, i1, i1, i1
        %17 = sv.wire sym @test_when_lazy_array_slice_driving_resolve.x {name="x"} : !hw.inout<i4>
        sv.assign %17, %15 : i4
        %16 = sv.read_inout %17 : !hw.inout<i4>
        hw.output %16 : i4
    }
}
