hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
    %0 = hw.constant 0 : i2
    %1 = hw.constant 1 : i2
    %2 = hw.constant 1 : i2
    %3 = hw.constant 0 : i2
    %4 = hw.constant 0 : i1
    %5 = hw.constant 1 : i1
    %10 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %10 : !hw.inout<i1>
    %11 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %11 : !hw.inout<i1>
    %12 = sv.reg : !hw.inout<i1>
    %8 = sv.read_inout %12 : !hw.inout<i1>
    %13 = sv.reg : !hw.inout<i1>
    %9 = sv.read_inout %13 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %10, %4 : i1
            sv.bpassign %11, %4 : i1
            sv.bpassign %12, %5 : i1
            sv.bpassign %13, %4 : i1
        } else {
            sv.bpassign %10, %5 : i1
            sv.bpassign %11, %4 : i1
            sv.bpassign %12, %4 : i1
            sv.bpassign %13, %4 : i1
        }
    }
    %14 = comb.concat %9, %8, %7, %6 : i1, i1, i1, i1
    %16 = sv.wire sym @test_when_lazy_array_slice.x {name="x"} : !hw.inout<i4>
    sv.assign %16, %14 : i4
    %15 = sv.read_inout %16 : !hw.inout<i4>
    hw.output %15 : i4
}
