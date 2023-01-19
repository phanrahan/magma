module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_overlap(%I: i4, %S: i1) -> (O: i4) {
        %0 = comb.extract %I from 0 : (i4) -> i1
        %1 = comb.extract %I from 1 : (i4) -> i1
        %2 = comb.concat %1, %0 : i1, i1
        %3 = comb.extract %I from 2 : (i4) -> i1
        %4 = comb.extract %I from 3 : (i4) -> i1
        %5 = comb.concat %4, %3 : i1, i1
        %7 = sv.reg : !hw.inout<i4>
        %6 = sv.read_inout %7 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %4, %3, %2 : i1, i1, i2
                sv.bpassign %7, %8 : i4
            } else {
                %9 = comb.concat %1, %0, %5 : i1, i1, i2
                sv.bpassign %7, %9 : i4
            }
        }
        %10 = comb.extract %6 from 0 : (i4) -> i2
        %11 = comb.extract %6 from 2 : (i4) -> i1
        %12 = comb.extract %6 from 3 : (i4) -> i1
        %13 = comb.concat %12, %11, %10 : i1, i1, i2
        hw.output %13 : i4
    }
}
