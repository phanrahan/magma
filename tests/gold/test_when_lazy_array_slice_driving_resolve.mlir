hw.module @test_when_lazy_array_slice_driving_resolve(%S: i1) -> (O: i4) {
    %0 = hw.constant 1 : i1
    %1 = hw.constant 2 : i4
    %2 = hw.constant 4 : i4
    %3 = hw.constant 0 : i1
    %4 = hw.constant 1 : i1
    %9 = sv.reg : !hw.inout<i1>
    %5 = sv.read_inout %9 : !hw.inout<i1>
    %10 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %10 : !hw.inout<i1>
    %11 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %11 : !hw.inout<i1>
    %12 = sv.reg : !hw.inout<i1>
    %8 = sv.read_inout %12 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %9, %3 : i1
            sv.bpassign %10, %4 : i1
            sv.bpassign %11, %3 : i1
            sv.bpassign %12, %3 : i1
        } else {
            sv.bpassign %9, %3 : i1
            sv.bpassign %10, %3 : i1
            sv.bpassign %11, %4 : i1
            sv.bpassign %12, %3 : i1
        }
    }
    %13 = comb.concat %8, %7, %6, %0 : i1, i1, i1, i1
    %15 = sv.wire sym @test_when_lazy_array_slice_driving_resolve.x {name="x"} : !hw.inout<i4>
    sv.assign %15, %13 : i4
    %14 = sv.read_inout %15 : !hw.inout<i4>
    hw.output %14 : i4
}
