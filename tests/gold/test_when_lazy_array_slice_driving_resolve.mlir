module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_driving_resolve(%S: i1) -> (O: i4) {
        %0 = hw.constant 1 : i1
        %1 = hw.constant 2 : i4
        %2 = hw.constant 4 : i4
        %3 = hw.constant 0 : i1
        %4 = hw.constant 1 : i1
        %6 = sv.reg : !hw.inout<i4>
        %5 = sv.read_inout %6 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %7 = comb.concat %3, %3, %4, %3 : i1, i1, i1, i1
                sv.bpassign %6, %7 : i4
            } else {
                %8 = comb.concat %3, %4, %3, %3 : i1, i1, i1, i1
                sv.bpassign %6, %8 : i4
            }
        }
        %9 = comb.extract %5 from 1 : (i4) -> i1
        %10 = comb.extract %5 from 2 : (i4) -> i1
        %11 = comb.extract %5 from 3 : (i4) -> i1
        %12 = comb.concat %11, %10, %9, %0 : i1, i1, i1, i1
        %14 = sv.wire sym @test_when_lazy_array_slice_driving_resolve.x name "x" : !hw.inout<i4>
        sv.assign %14, %12 : i4
        %13 = sv.read_inout %14 : !hw.inout<i4>
        hw.output %13 : i4
    }
}
