module attributes {circt.loweringOptions = "locationInfoStyle=none"} {
    hw.module @test_when_lazy_array_multiple_whens(%I: i4, %S: i1) -> (O: i4) {
        %1 = hw.constant -1 : i1
        %0 = comb.xor %1, %S : i1
        %3 = sv.reg name "_WHEN_WIRE_0" : !hw.inout<i4>
        %2 = sv.read_inout %3 : !hw.inout<i4>
        sv.alwayscomb {
            sv.if %S {
                %8 = comb.concat %5, %4, %7, %6 : i1, i1, i1, i1
                sv.bpassign %3, %8 : i4
            } else {
                %9 = comb.concat %7, %6, %5, %4 : i1, i1, i1, i1
                sv.bpassign %3, %9 : i4
            }
        }
        %4 = comb.extract %I from 2 : (i4) -> i1
        %5 = comb.extract %I from 3 : (i4) -> i1
        %6 = comb.extract %I from 0 : (i4) -> i1
        %7 = comb.extract %I from 1 : (i4) -> i1
        %10 = comb.extract %2 from 0 : (i4) -> i1
        %11 = comb.extract %I from 0 : (i4) -> i1
        %12 = comb.extract %2 from 1 : (i4) -> i1
        %13 = comb.extract %I from 1 : (i4) -> i1
        %14 = comb.extract %2 from 2 : (i4) -> i1
        %15 = comb.extract %I from 2 : (i4) -> i1
        %16 = comb.extract %2 from 3 : (i4) -> i1
        %17 = comb.extract %I from 3 : (i4) -> i1
        %22 = sv.reg name "_WHEN_WIRE_1" : !hw.inout<i1>
        %18 = sv.read_inout %22 : !hw.inout<i1>
        %23 = sv.reg name "_WHEN_WIRE_2" : !hw.inout<i1>
        %19 = sv.read_inout %23 : !hw.inout<i1>
        %24 = sv.reg name "_WHEN_WIRE_3" : !hw.inout<i1>
        %20 = sv.read_inout %24 : !hw.inout<i1>
        %25 = sv.reg name "_WHEN_WIRE_4" : !hw.inout<i1>
        %21 = sv.read_inout %25 : !hw.inout<i1>
        sv.alwayscomb {
            sv.bpassign %22, %10 : i1
            sv.bpassign %23, %12 : i1
            sv.bpassign %24, %14 : i1
            sv.bpassign %25, %16 : i1
            sv.if %0 {
                sv.bpassign %22, %11 : i1
                sv.bpassign %23, %13 : i1
                sv.bpassign %24, %15 : i1
                sv.bpassign %25, %17 : i1
            }
        }
        %26 = comb.concat %21, %20, %19, %18 : i1, i1, i1, i1
        sv.verbatim "WHEN_ASSERT_125: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %14, %15) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_126: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %16, %17) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_127: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %10, %11) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_128: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%S, %12, %13) : i1, i1, i1
        %27 = comb.xor %1, %S : i1
        sv.verbatim "WHEN_ASSERT_129: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %14, %11) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_130: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %16, %13) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_131: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %10, %15) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_132: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%27, %12, %17) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_133: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %18, %11) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_134: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %19, %13) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_135: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %20, %15) : i1, i1, i1
        sv.verbatim "WHEN_ASSERT_136: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%0, %21, %17) : i1, i1, i1
        %28 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_137: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%28, %18, %10) : i1, i1, i1
        %29 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_138: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%29, %19, %12) : i1, i1, i1
        %30 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_139: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%30, %20, %14) : i1, i1, i1
        %31 = comb.xor %1, %0 : i1
        sv.verbatim "WHEN_ASSERT_140: assert property (({{0}}) |-> ({{1}} == {{2}}));" (%31, %21, %16) : i1, i1, i1
        hw.output %26 : i4
    }
}
