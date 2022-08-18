hw.module @test_internal_instantiation_complex(%I: i2, %S: i2) -> (O: i1) {
    %0 = comb.extract %S from 0 : (i2) -> i1
    %1 = comb.extract %S from 1 : (i2) -> i1
    %2 = comb.extract %I from 0 : (i2) -> i1
    %3 = hw.constant 1 : i1
    %4 = comb.and %2, %3 : i1
    %5 = comb.extract %I from 1 : (i2) -> i1
    %6 = hw.constant 1 : i1
    %7 = comb.xor %5, %6 : i1
    %10 = sv.wire sym @test_internal_instantiation_complex.x {name="x"} : !hw.inout<i1>
    sv.assign %10, %8 : i1
    %9 = sv.read_inout %10 : !hw.inout<i1>
    %11 = hw.constant 1 : i1
    %13 = sv.reg : !hw.inout<i1>
    %8 = sv.read_inout %13 : !hw.inout<i1>
    %14 = sv.reg : !hw.inout<i1>
    %12 = sv.read_inout %14 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %0 {
            sv.bpassign %14, %9 : i1
            sv.if %1 {
                sv.bpassign %13, %4 : i1
            } else {
                sv.bpassign %13, %7 : i1
            }
        } else {
            sv.bpassign %14, %11 : i1
        }
    }
    hw.output %12 : i1
}
