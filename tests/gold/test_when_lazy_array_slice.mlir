hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
    %0 = hw.constant 0 : i1
    %1 = hw.constant 1 : i1
    %6 = sv.reg : !hw.inout<i1>
    %2 = sv.read_inout %6 : !hw.inout<i1>
    %7 = sv.reg : !hw.inout<i1>
    %3 = sv.read_inout %7 : !hw.inout<i1>
    %8 = sv.reg : !hw.inout<i1>
    %4 = sv.read_inout %8 : !hw.inout<i1>
    %9 = sv.reg : !hw.inout<i1>
    %5 = sv.read_inout %9 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %6, %0 : i1
            sv.bpassign %7, %0 : i1
            sv.bpassign %8, %1 : i1
            sv.bpassign %9, %0 : i1
        } else {
            sv.bpassign %6, %1 : i1
            sv.bpassign %7, %0 : i1
            sv.bpassign %8, %0 : i1
            sv.bpassign %9, %0 : i1
        }
    }
    %10 = comb.concat %5, %4, %3, %2 : i1, i1, i1, i1
    %12 = sv.wire sym @test_when_lazy_array_slice.x {name="x"} : !hw.inout<i4>
    sv.assign %12, %10 : i4
    %11 = sv.read_inout %12 : !hw.inout<i4>
    hw.output %11 : i4
}
