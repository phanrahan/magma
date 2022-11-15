module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_overlap(%I: i4, %S: i1) -> (O: i4) {
        %0 = comb.extract %I from 0 : (i4) -> i1
        %1 = comb.extract %I from 1 : (i4) -> i1
        %2 = comb.concat %1, %0 : i1, i1
        %3 = comb.extract %I from 2 : (i4) -> i1
        %4 = comb.extract %I from 3 : (i4) -> i1
        %5 = comb.concat %4, %3 : i1, i1
        %10 = sv.reg : !hw.inout<i4>
        %6 = sv.read_inout %10 : !hw.inout<i4>
        %11 = sv.reg : !hw.inout<i2>
        %7 = sv.read_inout %11 : !hw.inout<i2>
        %12 = sv.reg : !hw.inout<i1>
        %8 = sv.read_inout %12 : !hw.inout<i1>
        %13 = sv.reg : !hw.inout<i1>
        %9 = sv.read_inout %13 : !hw.inout<i1>
        sv.alwayscomb {
            sv.if %S {
                sv.bpassign %11, %2 : i2
                sv.bpassign %12, %3 : i1
                sv.bpassign %13, %4 : i1
            } else {
                sv.bpassign %11, %5 : i2
                sv.bpassign %12, %0 : i1
                sv.bpassign %13, %1 : i1
            }
        }
        %14 = comb.concat %9, %8, %7 : i1, i1, i2
        hw.output %14 : i4
    }
}
