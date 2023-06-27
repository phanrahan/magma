module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_slice_overlap(%I: i4, %S: i1) -> (O: i4) {
        %1 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i4>
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
        %13 = comb.concat %12, %11, %10 : i1, i1, i2
        %14 = comb.extract %I from 0 : (i4) -> i1
        %15 = comb.extract %I from 1 : (i4) -> i1
        %16 = comb.concat %15, %14 : i1, i1
        sv.verbatim "WHEN_ASSERT_0: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %16) : i1, i2, i2
        %17 = comb.extract %I from 2 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_1: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %11, %17) : i1, i1, i1
        %18 = comb.extract %I from 3 : (i4) -> i1
        sv.verbatim "WHEN_ASSERT_2: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %18) : i1, i1, i1
        %20 = hw.constant -1 : i1
        %19 = comb.xor %20, %S : i1
        %21 = comb.concat %18, %17 : i1, i1
        sv.verbatim "WHEN_ASSERT_3: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %10, %21) : i1, i2, i2
        sv.verbatim "WHEN_ASSERT_4: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %11, %14) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_5: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%19, %12, %15) : i1, i1, i1
        hw.output %13 : i4
    }
}
