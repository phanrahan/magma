hw.module @test_when_lazy_array_resolve(%S: i1) -> (O: i2) {
    %0 = hw.constant 1 : i2
    %2 = sv.wire sym @test_when_lazy_array_resolve.x {name="x"} : !hw.inout<i2>
    sv.assign %2, %0 : i2
    %1 = sv.read_inout %2 : !hw.inout<i2>
    %3 = comb.extract %1 from 0 : (i2) -> i1
    %4 = comb.extract %1 from 1 : (i2) -> i1
    %7 = sv.reg : !hw.inout<i1>
    %5 = sv.read_inout %7 : !hw.inout<i1>
    %8 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %8 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %7, %3 : i1
            sv.bpassign %8, %4 : i1
        } else {
            sv.bpassign %7, %4 : i1
            sv.bpassign %8, %3 : i1
        }
    }
    %9 = comb.concat %6, %5 : i1, i1
    hw.output %9 : i2
}
