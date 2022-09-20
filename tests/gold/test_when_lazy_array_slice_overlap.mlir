hw.module @test_when_lazy_array_slice_overlap(%I: i4, %S: i1) -> (O: i4) {
    %0 = comb.extract %I from 0 : (i4) -> i1
    %1 = comb.extract %I from 1 : (i4) -> i1
    %2 = comb.extract %I from 2 : (i4) -> i1
    %3 = comb.extract %I from 3 : (i4) -> i1
    %8 = sv.reg : !hw.inout<i1>
    %4 = sv.read_inout %8 : !hw.inout<i1>
    %9 = sv.reg : !hw.inout<i1>
    %5 = sv.read_inout %9 : !hw.inout<i1>
    %10 = sv.reg : !hw.inout<i1>
    %6 = sv.read_inout %10 : !hw.inout<i1>
    %11 = sv.reg : !hw.inout<i1>
    %7 = sv.read_inout %11 : !hw.inout<i1>
    sv.alwayscomb {
        sv.if %S {
            sv.bpassign %8, %0 : i1
            sv.bpassign %9, %1 : i1
            sv.bpassign %10, %2 : i1
            sv.bpassign %11, %3 : i1
        } else {
            sv.bpassign %8, %2 : i1
            sv.bpassign %9, %3 : i1
            sv.bpassign %10, %0 : i1
            sv.bpassign %11, %1 : i1
        }
    }
    %12 = comb.concat %7, %6, %5, %4 : i1, i1, i1, i1
    hw.output %12 : i4
}
