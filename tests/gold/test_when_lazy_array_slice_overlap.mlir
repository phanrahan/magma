module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_overlap(%I: i4, %S: i1) -> (O: i4) {
        %1 = sv.reg : !hw.inout<i4>
        %0 = sv.read_inout %1 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %5 = comb.concat %4, %3, %2 : i1, i1, i2
                sv.bpassign %1, %5 : i4
            } else {
                %9 = comb.concat %8, %7, %6 : i1, i1, i2
                sv.bpassign %1, %9 : i4
            }
        }
        %2 = comb.extract %I from 0 : (i4) -> i2
        %3 = comb.extract %I from 2 : (i4) -> i1
        %4 = comb.extract %I from 3 : (i4) -> i1
        %6 = comb.extract %I from 2 : (i4) -> i2
        %7 = comb.extract %I from 0 : (i4) -> i1
        %8 = comb.extract %I from 1 : (i4) -> i1
        %10 = comb.extract %0 from 0 : (i4) -> i2
        %11 = comb.extract %0 from 2 : (i4) -> i1
        %12 = comb.extract %0 from 3 : (i4) -> i1
        %13 = comb.concat %10, %11, %12 : i2, i1, i1
        hw.output %13 : i4
    }
}
