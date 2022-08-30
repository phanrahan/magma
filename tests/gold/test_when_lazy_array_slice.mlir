hw.module @test_when_lazy_array_slice(%S: i1) -> (O: i4) {
    %0 = hw.constant 0 : i2
    %1 = hw.constant 1 : i2
    %2 = hw.constant 1 : i2
    %3 = hw.constant 0 : i2
    %6 = sv.reg : !hw.inout<i2>
    %4 = sv.read_inout %6 : !hw.inout<i2>
    %7 = sv.reg : !hw.inout<i2>
    %5 = sv.read_inout %7 : !hw.inout<i2>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %6, %0 : i2
            sv.bpassign %7, %1 : i2
        } else {
            sv.bpassign %6, %2 : i2
            sv.bpassign %7, %3 : i2
        }
    }
    %8 = comb.extract %4 from 0 : (i2) -> i1
    %9 = comb.extract %4 from 1 : (i2) -> i1
    %10 = comb.extract %5 from 0 : (i2) -> i1
    %11 = comb.extract %5 from 1 : (i2) -> i1
    %12 = comb.concat %11, %10, %9, %8 : i1, i1, i1, i1
    %14 = sv.wire sym @test_when_lazy_array_slice.x {name="x"} : !hw.inout<i4>
    sv.assign %14, %12 : i4
    %13 = sv.read_inout %14 : !hw.inout<i4>
    hw.output %13 : i4
}
